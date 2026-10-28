# Layout 02 verification — 2026-09-08

## Maintenance audit — 2026-09-09

Audited the last committed layout without changing its geometry or component placements. Clearance booleans were resetting the main skin and ear materials to opaque; the model now preserves each part's color/alpha through those operations. Earlier claims of complete transparency were incorrect. Reviewed the corrected [isometric](iso_20260909T045100Z.png) and [rear](rear_20260909T045100Z.png) snapshots; the main skin and ears now reveal the mechanism.

Refreshed neutral and 56-pose fit checks: zero overlaps in the tested pairs, no active-display clipping, and all authored proxy solids valid. The previous neutral report contained a stale collision from an earlier layout. Validation scripts now fail explicitly on detected errors and publish complete JSON atomically. Neutral report descriptions now derive the actual pose count. The lower/inboard openings, shroud, wiring, actual mounting hardware and optics remain the documented unfinished fabrication work.

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

Historical September 8 snapshots: [isometric](iso_20260908T131833Z.png), [front](front_20260908T131833Z.png), [side](side_20260908T131833Z.png), [rear](rear_20260908T131833Z.png). These still contain opaque skin/ear surfaces caused by the material-reset bug corrected in the September 9 audit above. They must not be cited as proof of complete shell transparency. Viewer roll/pitch/yaw and shell-visibility controls were exercised during the original revision.

These are layout checks, not continuous swept clearance, manufacturing tolerance, complete cable routing, body clearance, optical validation or fabrication approval. Final servo selection, retention hardware, inserts, mounting patterns and moving harness details remain open; see the [layout report](../README.md).
