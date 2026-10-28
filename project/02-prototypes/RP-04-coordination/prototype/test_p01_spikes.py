"""P-01 virtual spikes. Exploratory; not G01/G03."""
import unittest

from p01_harness import Event, Sim, kinds, replay_ok
from score import P01, P02_BEHIND_BODY, P02_IN_SECTOR, validate_score
from wait_model import Cue, Wait, WaitEvent, wait_satisfied

ADAPTERS = ("TIME", "PROG", "HYBRID")


class SharedInvariants(unittest.TestCase):
    def test_happy_hold_and_replay(self):
        for a in ADAPTERS:
            s = Sim(a)
            log = s.run()
            self.assertTrue(kinds(log, "accept", "base"))
            self.assertFalse(s.base_motion)
            self.assertTrue(kinds(log, "dispatch", "head"))
            self.assertTrue(replay_ok(a))

    def test_cancel_no_search(self):
        for a in ADAPTERS:
            s = Sim(a, "cancel")
            log = s.run()
            self.assertTrue(any(e.reason == "OX-CANCEL" for e in log))
            after = [e for e in log if e.t > 400_000 and e.kind == "dispatch" and e.cue_id == "P01-C04"]
            self.assertEqual(after, [])
            self.assertTrue(replay_ok(a, "cancel"))

    def test_preempt_new_epoch_gaze(self):
        for a in ADAPTERS:
            s = Sim(a, "preempt")
            log = s.run()
            self.assertTrue(s.p02_gaze)
            self.assertFalse(s.search_success)
            gaze = [e for e in log if e.cue_id == "P02-C01"]
            self.assertTrue(gaze)
            self.assertGreater(gaze[0].epoch, 1)
            self.assertTrue(replay_ok(a, "preempt"))

    def test_stale_rejected(self):
        for a in ADAPTERS:
            log = Sim(a, "stale").run()
            self.assertTrue(any(e.reason == "stale_epoch" for e in log))
            self.assertTrue(replay_ok(a, "stale"))

    def test_deny_face_no_onset(self):
        for a in ADAPTERS:
            log = Sim(a, "deny_face").run()
            self.assertTrue(any(e.reason == "denied" and e.channel == "face" for e in log))
            self.assertFalse(kinds(log, "source_onset", "face"))
            self.assertTrue(replay_ok(a, "deny_face"))


class Discriminating(unittest.TestCase):
    def test_delay_head_logged(self):
        for a in ADAPTERS:
            log = Sim(a, "delay_head").run()
            self.assertTrue(any(e.kind == "delay" for e in log), a)
            self.assertTrue(replay_ok(a, "delay_head"), a)

    def test_time_invalid(self):
        time_denies = any(e.reason == "time_model_invalid" for e in Sim("TIME", "time_invalid").run())
        prog_denies = any(e.reason == "time_model_invalid" for e in Sim("PROG", "time_invalid").run())
        hybrid = Sim("HYBRID", "time_invalid").run()
        hybrid_time = [e for e in hybrid if e.reason == "time_model_invalid"]
        self.assertTrue(time_denies)
        self.assertFalse(prog_denies)
        self.assertTrue(hybrid_time)
        self.assertTrue(replay_ok("HYBRID", "time_invalid"))

    def test_stuck_progress(self):
        time_c04 = any(e.cue_id == "P01-C04" and e.kind == "dispatch" for e in Sim("TIME", "stuck_progress").run())
        prog_c04 = any(e.cue_id == "P01-C04" and e.kind == "dispatch" for e in Sim("PROG", "stuck_progress").run())
        hyb_c04 = any(e.cue_id == "P01-C04" and e.kind == "dispatch" for e in Sim("HYBRID", "stuck_progress").run())
        self.assertTrue(time_c04)
        self.assertFalse(prog_c04)
        self.assertFalse(hyb_c04)
        self.assertTrue(replay_ok("HYBRID", "stuck_progress"))

    def test_restart_no_resume(self):
        for a in ADAPTERS:
            s = Sim(a, "restart")
            log = s.run()
            self.assertTrue(any(e.reason == "OX-RESTART" for e in log))
            resumed = [
                e for e in log
                if e.t > 400_000 and e.kind in ("source_onset", "accept") and e.channel == "head" and e.epoch == 1
            ]
            self.assertEqual(resumed, [], a)
            self.assertTrue(replay_ok(a, "restart"), a)


class HybridWaitLanguage(unittest.TestCase):
    def test_deny_face_still_rises_on_light(self):
        s = Sim("HYBRID", "deny_face")
        log = s.run()
        self.assertFalse(kinds(log, "source_onset", "face"))
        self.assertTrue(kinds(log, "source_onset", "light"))
        self.assertTrue(any(e.cue_id == "P01-C03" and e.kind == "dispatch" for e in log))
        self.assertTrue(replay_ok("HYBRID", "deny_face"))

    def test_deny_light_still_rises_on_face(self):
        s = Sim("HYBRID", "deny_light")
        log = s.run()
        self.assertFalse(kinds(log, "source_onset", "light"))
        self.assertTrue(kinds(log, "source_onset", "face"))
        self.assertTrue(any(e.cue_id == "P01-C03" and e.kind == "dispatch" for e in log))
        self.assertTrue(replay_ok("HYBRID", "deny_light"))

    def test_both_visible_denied_does_not_hang(self):
        s = Sim("HYBRID", "deny_visible")
        log = s.run()
        self.assertFalse(kinds(log, "source_onset", "face"))
        self.assertFalse(kinds(log, "source_onset", "light"))
        c03 = [e for e in log if e.cue_id == "P01-C03"]
        self.assertTrue(c03)
        self.assertTrue(any(e.reason == "OX-DELAY" for e in c03))
        self.assertTrue(replay_ok("HYBRID", "deny_visible"))

    def test_c04_uses_named_threshold_not_clock(self):
        hyb = Sim("HYBRID").run()
        progress = [e for e in hyb if e.kind == "progress" and e.cue_id == "P01-C03"]
        self.assertTrue(progress)
        self.assertEqual(progress[0].reason, "HM-03.rise_commit")
        c04 = [e for e in hyb if e.cue_id == "P01-C04" and e.kind == "dispatch"]
        self.assertTrue(c04)
        self.assertGreaterEqual(c04[0].t, progress[0].t)
        self.assertTrue(any(e.kind == "target_decision" for e in hyb))

    def test_target_branch_dispatches_hm05(self):
        s = Sim("HYBRID", "target")
        log = s.run()
        self.assertTrue(s.search_success)
        self.assertTrue(any(e.cue_id == "P01-C04" and e.kind == "dispatch" for e in log))
        self.assertTrue(replay_ok("HYBRID", "target"))

    def test_deadline_expiry_on_stuck_search(self):
        log = Sim("HYBRID", "stuck_progress").run()
        self.assertFalse(any(e.cue_id == "P01-C04" and e.kind == "dispatch" for e in log))
        self.assertTrue(any(e.cue_id == "P01-C04" and e.reason == "OX-DELAY" for e in log))

    def test_cancel_during_wait(self):
        s = Sim("HYBRID", "cancel_wait")
        log = s.run()
        self.assertTrue(any(e.reason == "OX-CANCEL" for e in log))
        after = [e for e in log if e.t >= 200_000 and e.kind == "dispatch" and e.cue_id == "P01-C03"]
        self.assertEqual(after, [])
        self.assertTrue(replay_ok("HYBRID", "cancel_wait"))

    def test_stale_after_epoch_flush(self):
        log = Sim("HYBRID", "stale").run()
        self.assertTrue(any(e.reason == "stale_epoch" for e in log))
        self.assertFalse(any(e.kind == "source_onset" and e.cue_id == "P01-C04" and e.epoch == 1 for e in log if e.t > 500_000))

    def test_dispatch_and_receipt_are_not_onset(self):
        wait = Wait("event", (WaitEvent("face", "source_onset"),), deadline_us=300_000, on_deadline="degrade")
        log = (
            Event(100_000, "dispatch", "face", 1, "P01-C02"),
            Event(100_000, "receipt", "face", 1, "P01-C02"),
            Event(100_000, "accept", "face", 1, "P01-C02"),
        )
        self.assertFalse(wait_satisfied(wait, log, 1))
        onset = log + (Event(120_000, "source_onset", "face", 1, "P01-C02"),)
        self.assertTrue(wait_satisfied(wait, onset, 1))
        stale = (Event(120_000, "source_onset", "face", 1, "P01-C02"),)
        self.assertFalse(wait_satisfied(wait, stale, 2))


class ScoreValidator(unittest.TestCase):
    def test_registered_scores_pass(self):
        self.assertEqual(validate_score("P01", P01), [])
        self.assertEqual(validate_score("P02_IN_SECTOR", P02_IN_SECTOR), [])
        self.assertEqual(validate_score("P02_BEHIND_BODY", P02_BEHIND_BODY), [])

    def test_behind_body_names_counter_yaw(self):
        self.assertTrue(any(c.primitive == "counter_yaw" for c in P02_BEHIND_BODY))
        self.assertTrue(any(c.panel == "BM-05" for c in P02_BEHIND_BODY))
        self.assertTrue(any(c.panel == "BM-01" for c in P02_IN_SECTOR))

    def test_rejects_unqualified_progress(self):
        bad = (
            Cue("P01-C03", "head", "HM-03", "progress", 0,
                wait=Wait("event", (WaitEvent("head", "progress", "P01-C02"),), deadline_us=1, on_deadline="deny"),
                fallback="OX-DELAY"),
        )
        self.assertTrue(any("unqualified progress" in e for e in validate_score("P01", bad)))

    def test_rejects_missing_deadline_and_fallback(self):
        bad = (
            Cue("P01-C03", "head", "HM-03", "progress", 0,
                wait=Wait("event", (WaitEvent("face", "source_onset"),))),
        )
        errors = validate_score("P01", bad)
        self.assertTrue(any("missing deadline" in e for e in errors))
        self.assertTrue(any("absent fallback" in e for e in errors))

    def test_rejects_unknown_event_duplicate_and_cross_epoch(self):
        wait = Wait(
            "event",
            (WaitEvent("face", "dispatch", cue_id="P02-C01", epoch="old"),),
            deadline_us=1,
            on_deadline="deny",
        )
        bad = (
            Cue("P01-C02", "face", "E-open", "time", 0, fallback="OX-DENY(face)"),
            Cue("P01-C02", "face", "E-open", "time", 0, fallback="OX-DENY(face)"),
            Cue("P01-C03", "head", "HM-03", "progress", 0, wait=wait, fallback="OX-DELAY"),
        )
        errors = validate_score("P01", bad)
        self.assertTrue(any("duplicate cue identity" in e for e in errors))
        self.assertTrue(any("unknown event name" in e or "not source onset" in e for e in errors))
        self.assertTrue(any("cross-epoch" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
