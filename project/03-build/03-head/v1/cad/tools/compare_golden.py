"""Compare head check outputs with a source-matched, immutable golden set.

Rebaseline only after the source revision and all checks have been reviewed.
The default comparison deliberately checks every field, including hit order.
"""

import argparse
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = (
    "revision-checks.json",
    "generated/feetech-mounts.json",
    "generated/fastener-stack.json",
    "motion-envelope.json",
    "mass-placement.json",
)
PROVENANCE_KEYS = {"source_sha256", "generated_at", "runtime_s", "elapsed_s"}


def tolerance(path):
    key = str(path[-1]).lower() if path else ""
    if "volume" in key or key.endswith("_mm3"):
        return 0.01
    if key.endswith("_mm") or "distance" in key or "clearance" in key or "gap" in key:
        return 0.001
    # Binary BRep reload can change the final few floating point bits of
    # mass properties without changing the modeled solid.
    return 1e-9


def compare(expected, actual, path=()):
    """Yield human-readable mismatches without weakening hit or pair checks."""
    if type(expected) is not type(actual):
        yield f"{path}: type {type(expected).__name__} != {type(actual).__name__}"
    elif isinstance(expected, dict):
        akeys, bkeys = expected.keys() - PROVENANCE_KEYS, actual.keys() - PROVENANCE_KEYS
        if akeys != bkeys:
            yield f"{path}: keys {sorted(akeys)} != {sorted(bkeys)}"
        for key in akeys & bkeys:
            yield from compare(expected[key], actual[key], (*path, key))
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            yield f"{path}: length {len(expected)} != {len(actual)}"
        for index, (a, b) in enumerate(zip(expected, actual)):
            yield from compare(a, b, (*path, index))
    elif isinstance(expected, (float, int)) and not isinstance(expected, bool):
        if not math.isclose(expected, actual, rel_tol=0, abs_tol=tolerance(path)):
            yield f"{path}: {expected} != {actual}"
    elif expected != actual:
        yield f"{path}: {expected!r} != {actual!r}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--golden", type=Path, default=ROOT / "golden")
    parser.add_argument("--actual", type=Path, default=ROOT)
    parser.add_argument("--allow-missing", action="store_true", help="For pre-D-049 checkouts only")
    args = parser.parse_args()
    failed = False
    for name in OUTPUTS:
        gold, current = args.golden / name, args.actual / name
        if not gold.is_file() or not current.is_file():
            print(f"{'SKIP' if args.allow_missing else 'FAIL'} {name}: missing golden or output")
            failed |= not args.allow_missing
            continue
        differences = list(compare(json.loads(gold.read_text()), json.loads(current.read_text())))
        print(f"{'FAIL' if differences else 'PASS'} {name}: {len(differences)} differences")
        for item in differences[:20]:
            print("  ", item)
        failed |= bool(differences)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
