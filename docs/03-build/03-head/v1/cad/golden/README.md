# Golden head check outputs

The outputs were copied from commit `1758d69` (D-048) before the performance
work began. Its `mass-placement.json` proved stale: its first part row said
16.81 g while the same commit's `revision-checks.json` volume implies 18.68 g.
An uncached `mass_layout.py` run confirmed the latter. The original mass file
is preserved in `stale/mass-placement-1758d69.json`; the active mass golden is
the verified source-derived output. The other goldens remain byte copies.
`generated/feetech-mounts.json` does not exist at this commit: D-049 is still
uncommitted in the main checkout.

After D-049 lands, run every full check on that exact source, review the
results, and replace this directory with those outputs. Then run
`python tools/compare_golden.py` without `--allow-missing`.

Do not silently rebaseline in the comparator or runner. The checked in files
are independent evidence, not products of the current command.
