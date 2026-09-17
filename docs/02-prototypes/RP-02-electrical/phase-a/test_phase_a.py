"""Exploratory host checks; not G04/G05 scored evidence."""
import unittest

from codec import Frame, MessageType, decode, encode
from runtime import AuthorityLease, HeadController, Motion, TimeSample, fit_time_model


BOOT = bytes(range(16))


class CodecTests(unittest.TestCase):
    def test_round_trip_and_corruption(self):
        frame = Frame(MessageType.HEAD_GOAL, 19, BOOT, 7, 123456789, b"\x00a\x00b")
        wire = encode(frame)
        self.assertEqual(wire.hex(),
                         "0401051301110102030405060708090a0b0c0d0e0f0701010515cd5b0701010102040261046207a400")
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
