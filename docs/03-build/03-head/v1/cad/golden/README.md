# Golden head check outputs

The five active outputs are byte copies from the committed D-049 source at
`54a3533`, before the check-speed changes were applied to it. They are the
reference for full-grid sign-off. Run `python tools/compare_golden.py` without
`--allow-missing` after regenerating all five outputs on this branch.

The D-048 commit `1758d69` had a stale `mass-placement.json`: its first part
row said 16.81 g while its revision volume implies 18.68 g. That original is
preserved in `stale/mass-placement-1758d69.json` for the audit trail.

Do not silently rebaseline in the comparator or runner. The checked in files
are independent evidence, not products of the current command.
