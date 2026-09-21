"""Exploratory host checks; not G04/G05 scored evidence."""
import unittest

from codec import Frame, MessageType, decode, encode, LAYOUT_REVISION
from payloads import (
    BASE_STATE,
    BaseState,
    CueIdentity,
    HeadGoal,
    Nack,
    NackReason,
    command_nack,
    pack_base_state,
    pack_head_goal,
    pack_nack,
    unpack_base_state,
    unpack_head_goal,
    unpack_nack,
)
from runtime import AuthorityLease, HeadController, Motion, TimeSample, fit_time_model


BOOT = bytes(range(16))


class CodecTests(unittest.TestCase):
    def test_round_trip_and_corruption(self):
        frame = Frame(MessageType.HEAD_GOAL, 19, BOOT, 7, 123456789, b"\x00a\x00b")
        wire = encode(frame)
        self.assertEqual(wire.hex(),
                         "0402051301110102030405060708090a0b0c0d0e0f0701010515cd5b07010101020402610462fba800")
        self.assertEqual(decode(wire), frame)
        damaged = bytearray(wire)
        damaged[10] ^= 1
        with self.assertRaises(ValueError):
            decode(bytes(damaged))

    def test_payload_boundary(self):
        frame = Frame(MessageType.HEARTBEAT, 0, BOOT, 1, 0, bytes(64))
        self.assertEqual(decode(encode(frame)), frame)
        with self.assertRaises(ValueError):
            encode(Frame(MessageType.HEARTBEAT, 0, BOOT, 1, 0, bytes(65)))


class CoordinationPayloadTests(unittest.TestCase):
    def test_layout_revision_and_new_types(self):
        self.assertEqual(LAYOUT_REVISION, 2)
        self.assertEqual(int(MessageType.FACE_REPORT), 16)
        self.assertEqual(int(MessageType.LIGHT_REPORT), 17)
        self.assertEqual(int(MessageType.BASE_STATE), 23)
        self.assertEqual(int(MessageType.NACK), 13)

    def test_head_goal_round_trip_on_wire(self):
        goal = HeadGoal(CueIdentity(7, 11, 4), 1_000_000, 3, 1, 2, 100, 0, -50, 250, 2_000_000, 1)
        payload = pack_head_goal(goal)
        frame = Frame(MessageType.HEAD_GOAL, 8, BOOT, 3, 9, payload)
        self.assertEqual(unpack_head_goal(decode(encode(frame)).payload), goal)

    def test_base_state_fits_without_dropping_safety(self):
        self.assertEqual(BASE_STATE.size, 62)
        self.assertLessEqual(BASE_STATE.size, 64)
        state = BaseState(
            CueIdentity(1, 2, 3), 10, 11, 40, 100, -3, 4, 5, 6,
            7, 8, 9, 10, 11, 12, 1, 2, 0x00FF, 17,
        )
        raw = pack_base_state(state)
        self.assertEqual(len(raw), 62)
        self.assertEqual(unpack_base_state(raw), state)
        frame = Frame(MessageType.BASE_STATE, 1, BOOT, 1, 0, raw)
        self.assertEqual(decode(encode(frame)).payload, raw)

    def test_nack_time_late_stale_round_trip(self):
        for reason in (NackReason.TIME_MODEL_INVALID, NackReason.LATE, NackReason.STALE_EPOCH):
            nack = Nack(21, CueIdentity(4, 5, 6), reason)
            frame = Frame(MessageType.NACK, 21, BOOT, 5, 0, pack_nack(nack))
            self.assertEqual(unpack_nack(decode(encode(frame)).payload).reason, reason)

    def test_scheduled_reject_reasons(self):
        common = dict(valid_until_us=5_000, now_us=0, cmd_epoch=1, lateness_window_us=50)
        self.assertEqual(
            command_nack(start_at_us=100, time_model_valid=False, current_epoch=1, **common),
            NackReason.TIME_MODEL_INVALID,
        )
        self.assertEqual(
            command_nack(start_at_us=100, time_model_valid=True, current_epoch=1,
                         valid_until_us=5_000, now_us=200, cmd_epoch=1, lateness_window_us=50),
            NackReason.LATE,
        )
        self.assertEqual(
            command_nack(start_at_us=100, time_model_valid=True, current_epoch=3, **common),
            NackReason.STALE_EPOCH,
        )
        self.assertIsNone(
            command_nack(start_at_us=100, time_model_valid=True, current_epoch=1, **common),
        )


class SafetyTests(unittest.TestCase):
    def armed(self):
        c2 = HeadController(150_000, motor_present=True)
        self.assertTrue(c2.new_session(BOOT, 1, c2.boot_challenge))
        self.assertTrue(c2.heartbeat(BOOT, 1, 1, 0))
        self.assertTrue(c2.set_limits(BOOT, 1, 2, True))
        self.assertTrue(c2.enable(BOOT, 1, 3, 123, 1000))
        return c2

    def test_two_phase_arm_and_expiry_at_execution(self):
        c2 = HeadController(150_000, motor_present=True)
        self.assertTrue(c2.new_session(BOOT, 1, c2.boot_challenge))
        self.assertFalse(c2.enable(BOOT, 1, 1, 123, 0))
        c2 = self.armed()
        self.assertFalse(c2.goal(BOOT, 1, 4, 100, 101))
        self.assertTrue(c2.goal(BOOT, 1, 4, 2000, 101))
        self.assertFalse(c2.execute(2001))
        self.assertFalse(c2.execute(2001))

    def test_heartbeat_loss_and_no_replay(self):
        c2 = self.armed()
        self.assertTrue(c2.goal(BOOT, 1, 4, 300_000, 2000))
        c2.tick(150_001)
        self.assertEqual(c2.state, Motion.BRAKING)
        self.assertFalse(c2.pending_goals)
        c2.brake_complete()
        c2.clear_fault()
        self.assertTrue(c2.heartbeat(BOOT, 1, 5, 151_000))
        self.assertFalse(c2.enable(BOOT, 1, 6, 123, 152_000))
        self.assertTrue(c2.set_limits(BOOT, 1, 6, True))
        self.assertFalse(c2.enable(BOOT, 1, 7, 123, 152_000))
        self.assertTrue(c2.enable(BOOT, 1, 7, 124, 152_000))
        self.assertFalse(c2.goal(BOOT, 1, 4, 300_000, 152_000))

    def test_estop_and_session_epoch(self):
        c2 = self.armed()
        c2.estop()
        self.assertEqual(c2.state, Motion.INHIBITED)
        c2.motor_present = True
        c2.clear_fault()
        self.assertFalse(c2.goal(BOOT, 1, 4, 300_000, 2000))
        self.assertFalse(c2.new_session(BOOT, 1, c2.boot_challenge))
        self.assertTrue(c2.new_session(BOOT, 2, c2.boot_challenge))
        self.assertFalse(c2.enable(BOOT, 1, 5, 124, 3000))

    def test_cold_boot_rejects_old_session(self):
        c2 = self.armed()
        old_challenge = c2.boot_challenge
        c2.reset(reboot=True)
        self.assertNotEqual(old_challenge, c2.boot_challenge)
        self.assertFalse(c2.new_session(BOOT, 1, old_challenge))
        self.assertTrue(c2.new_session(BOOT, 2, c2.boot_challenge))

    def test_lease_requires_action_progress(self):
        lease = AuthorityLease(100_000)
        self.assertFalse(lease.renew(BOOT, 1, 0, False))
        self.assertTrue(lease.renew(BOOT, 1, 0, True))
        self.assertTrue(lease.alive(100_000))
        self.assertFalse(lease.alive(100_001))


class TimeTests(unittest.TestCase):
    def test_offset_and_raw_local_conversion(self):
        samples = [TimeSample(t, t + 1050, t + 1150, t + 200) for t in (0, 1_000_000, 2_000_000)]
        model = fit_time_model(samples)
        self.assertTrue(model.valid)
        self.assertAlmostEqual(model.to_master(3_001_000), 3_000_000, delta=1)
        self.assertGreaterEqual(model.uncertainty_us, 0)


if __name__ == "__main__":
    unittest.main()
