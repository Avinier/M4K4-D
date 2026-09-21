"""P-01 virtual spikes. Exploratory; not G01/G03."""
import unittest

from p01_harness import Sim, kinds, replay_ok

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

    def test_preempt_new_epoch_gaze(self):
        for a in ADAPTERS:
            s = Sim(a, "preempt")
            log = s.run()
            self.assertTrue(s.p02_gaze)
            self.assertFalse(s.search_success)
            gaze = [e for e in log if e.cue_id == "P02-C01"]
            self.assertTrue(gaze)
            self.assertGreater(gaze[0].epoch, 1)

    def test_stale_rejected(self):
        for a in ADAPTERS:
            log = Sim(a, "stale").run()
            self.assertTrue(any(e.reason == "stale_epoch" for e in log))

    def test_deny_face_no_onset(self):
        for a in ADAPTERS:
            log = Sim(a, "deny_face").run()
            self.assertTrue(any(e.reason == "denied" and e.channel == "face" for e in log))
            self.assertFalse(kinds(log, "source_onset", "face"))


class Discriminating(unittest.TestCase):
    def test_delay_head_logged(self):
        for a in ADAPTERS:
            log = Sim(a, "delay_head").run()
            self.assertTrue(any(e.kind == "delay" for e in log), a)

    def test_time_invalid(self):
        time_denies = any(e.reason == "time_model_invalid" for e in Sim("TIME", "time_invalid").run())
        prog_denies = any(e.reason == "time_model_invalid" for e in Sim("PROG", "time_invalid").run())
        hybrid = Sim("HYBRID", "time_invalid").run()
        hybrid_time = [e for e in hybrid if e.reason == "time_model_invalid"]
        self.assertTrue(time_denies)
        self.assertFalse(prog_denies)
        self.assertTrue(hybrid_time)

    def test_stuck_progress(self):
        time_c04 = any(e.cue_id == "P01-C04" and e.kind == "dispatch" for e in Sim("TIME", "stuck_progress").run())
        prog_c04 = any(e.cue_id == "P01-C04" and e.kind == "dispatch" for e in Sim("PROG", "stuck_progress").run())
        hyb_c04 = any(e.cue_id == "P01-C04" and e.kind == "dispatch" for e in Sim("HYBRID", "stuck_progress").run())
        self.assertTrue(time_c04)
        self.assertFalse(prog_c04)
        self.assertFalse(hyb_c04)

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


if __name__ == "__main__":
    unittest.main()
