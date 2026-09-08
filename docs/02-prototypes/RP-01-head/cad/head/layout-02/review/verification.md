# Layout 02 verification — 2026-09-08

Final geometry includes the integrated crown rear wall. STEP generation and inspection used the text-to-cad 0.4.28 runtime. The stale derived imported-STEP inspection cache was removed before final inspection; the fresh export hash is `9fe7bb477f727db0eed9f874a7cb348e12225eeca392b848dc2e3385a78d80a1`.

| Check | Result |
|---|---|
| Exported assembly bounds | X −115…0, Y −75…75, Z −60…102 mm. The 162 mm total includes the 60 mm neck allocation. |
| Full authored-solid validation | 54 occurrences, zero failures, including self-intersection checks. |
| Whole assembly topology validation | 715 solid occurrences, zero failures. Self-intersection checks skipped for this whole-assembly pass; catalog solids retain their imported detail. |
| Motion overlap checks | 56 discrete pitch/roll poses × 159 tested pairs = 8,904 checks; zero overlapping tested pairs. |
| Neutral non-fastener assembly checks | Zero overlapping tested pairs; C2 upper USB service reserve clear. |
| Display exposure | Full 95.04 × 53.86 mm active rectangle exposed; minimum corner-to-diagonal aperture margin approximately 0.742 mm. |
| Camera/display separation | 1 mm vertical board-envelope gap. |
| LED package | Entire reserve inside crown; lower edge 3.3 mm above main roof. |
| Roll bearing spacing | 22 mm between centres. |
| Catalog integrity | All 631 camera solids and all 15 solids of each servo retained, with rigid transforms only. |

Reports: [refs](refs-final.json), [authored validation](validate-authored.json), [all topology](validate-all-topology.json), [bearing measurement](bearing-spacing.json), [motion](../fit-checks.json), [neutral fit](../assembly-checks.json).

Final plugin snapshots: [isometric](iso_20260908T131833Z.png), [front](front_20260908T131833Z.png), [side](side_20260908T131833Z.png), [rear](rear_20260908T131833Z.png). The complete front, side, rear and ear enclosure parts are translucent in this review packet so the internal arrangement is visible through the whole head. Front, isometric and rear images were visually reviewed after the final export; the closed crown back, clipped outlines and transparent ear shells are visible. Viewer roll/pitch/yaw and shell-visibility controls were also exercised during this revision.

These are layout checks, not continuous swept clearance, manufacturing tolerance, complete cable routing, body clearance, optical validation or fabrication approval. Final servo selection, retention hardware, inserts, mounting patterns and moving harness details remain open; see the [layout report](../README.md).
