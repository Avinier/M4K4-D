"""Incremental head v1 checks. Run from any directory with the CAD Python.

The full grid is for sign-off. --fast writes separate revision/fastener files.
Missing D-049 checks remain visible as unavailable until that source is merged.
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BODY = ROOT.parents[2] / "02-body" / "v1" / "cad"
CHASSIS = ROOT.parents[2] / "01-chassis" / "v1" / "cad"
BODY_PURCHASED = (ROOT.parents[3] / "02-prototypes" / "RP-06-cad" /
                  "body-chassis" / "layout-01" / "references" / "purchased")
STATE = ROOT / ".cache" / "run-checks.json"


@dataclass(frozen=True)
class Check:
    name: str
    cwd: Path
    script: str
    args: tuple[str, ...]
    output: Path


def source_files(check):
    # Deliberately broad: a newly imported helper or purchased part must
    # invalidate the result even if a hand-maintained dependency list misses it.
    roots = (ROOT, BODY, CHASSIS) if check.cwd == BODY else (ROOT,)
    files = []
    for root in roots:
        files.extend(root.glob("*.py"))
        files.extend((root / "purchased").rglob("*"))
    if check.cwd == BODY:
        files.extend(path for path in BODY_PURCHASED.rglob("*")
                     if path.suffix.lower() in (".step", ".stp") and
                     "__cadgen__" not in path.parts)
    if check.cwd not in roots:
        files.extend(check.cwd.glob("*.py"))
    files.append(check.cwd / check.script)
    if check.name != "envelope":
        files.append(ROOT / "motion-envelope.json")
    if check.name not in ("mass", "envelope"):
        files.append(ROOT / "mass-placement.json")
    return sorted({p for p in files if p.is_file()})


def fingerprint(check):
    digest = hashlib.sha256()
    digest.update(json.dumps([check.name, check.args]).encode())
    for path in source_files(check):
        digest.update(str(path.relative_to(ROOT.parents[3])).encode())
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def worker_cap():
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total // (1024 ** 3)
    except ImportError:
        ram_gb = 2
    cap = max(1, min(os.cpu_count() or 1, ram_gb // 2))
    return min(cap, max(1, int(os.environ.get("MAKAD_CHECK_WORKERS", cap))))


def execute(check, prior, force, workers=None):
    if not (check.cwd / check.script).is_file():
        return (check.name, "unavailable", 0.0, "source file missing", None)
    key = fingerprint(check)
    old = prior.get(check.name, {})
    if (not force and old.get("input") == key and old.get("output") == file_hash(check.output)
            and check.output.is_file() and old.get("passed")):
        return (check.name, "cached", 0.0, "", old)
    start = time.monotonic()
    environment = os.environ.copy()
    if workers is not None:
        environment["MAKAD_CHECK_WORKERS"] = str(workers)
    proc = subprocess.run([sys.executable, check.script, *check.args], cwd=check.cwd,
                          env=environment,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    elapsed = time.monotonic() - start
    logs = ROOT / ".cache" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    log = logs / (check.name + ".log")
    log.write_text(proc.stdout)
    produced = check.output.is_file()
    record = dict(input=key, output=file_hash(check.output),
                  passed=proc.returncode == 0 and produced,
                  runtime_s=round(elapsed, 3), log=str(log))
    detail = f"exit {proc.returncode}; {log}"
    if not produced:
        detail += f"; missing output {check.output}"
    return (check.name, "pass" if record["passed"] else "fail", elapsed,
            detail, record)


def run_stage(checks, prior, force, parallel=True):
    heavy = {"revision", "mounts", "clearance"}
    available = [check for check in checks if (check.cwd / check.script).is_file()]
    heavy_count = sum(check.name in heavy for check in available)
    light_count = len(available) - heavy_count
    share = max(1, (worker_cap() - light_count) // heavy_count) if heavy_count else None
    def submit(pool, check):
        return pool.submit(execute, check, prior, force,
                           share if check.name in heavy else None)
    if parallel and len(checks) > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(worker_cap(), len(checks))) as pool:
            futures = [submit(pool, check) for check in checks]
            return [future.result() for future in futures]
    return [execute(check, prior, force, share if check.name in heavy else None) for check in checks]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fast", action="store_true", help="3 x 3 pose grid; exploratory run")
    parser.add_argument("--solve", action="store_true", help="recalculate A0 axes before checks")
    parser.add_argument("--force", action="store_true", help="run even when inputs and outputs match")
    args = parser.parse_args()
    STATE.parent.mkdir(exist_ok=True)
    prior = json.loads(STATE.read_text()) if STATE.is_file() else {}
    results = []

    def stage(checks, parallel=True, force=None):
        batch = run_stage(checks, prior, args.force if force is None else force, parallel)
        results.extend(batch)
        for name, status, _, _, record in batch:
            if record is not None:
                prior[name] = record
        temporary = STATE.with_suffix(".tmp")
        temporary.write_text(json.dumps(prior, indent=2) + "\n")
        temporary.replace(STATE)
        return all(status in ("pass", "cached") for _, status, _, _, _ in batch)

    if args.solve:
        if not stage([Check("mass", ROOT, "mass_layout.py", ("--solve",), ROOT / "mass-placement.json")], False, True):
            return summary(results)
    elif not stage([Check("mass", ROOT, "mass_layout.py", (), ROOT / "mass-placement.json")], False):
        return summary(results)
    if not stage([Check("envelope", ROOT, "motion_envelope.py", ("--write",), ROOT / "motion-envelope.json")], False):
        return summary(results)

    first = [
        Check("revision", ROOT, "check_revision.py", ("--fast",) if args.fast else (),
              ROOT / ("revision-fast.json" if args.fast else "revision-checks.json")),
        Check("mounts", ROOT, "check_feetech_mounts.py", ("--fast",) if args.fast else (),
              ROOT / ("generated/feetech-mounts-fast.json" if args.fast else
                      "generated/feetech-mounts.json")),
        Check("integration", ROOT, "check_integration.py", (), ROOT / "generated/integration-fit.json"),
        Check("busy_minute", ROOT, "busy_minute.py", (), ROOT / "generated/busy-minute-d049.json"),
    ]
    second = [
        Check("clearance", ROOT, "check_layout.py", ("--fast",) if args.fast else (),
              ROOT / ("fit-fast.json" if args.fast else "fit-checks.json")),
        Check("fasteners", ROOT, "check_fasteners.py", ("--fast",) if args.fast else (),
              ROOT / ("generated/fastener-stack-fast.json" if args.fast else "generated/fastener-stack.json")),
    ]
    stage(first)
    stage(second)
    # FEA can consume substantially more than the 2 GiB assumed per OCC
    # worker, so give it the machine after the independent CAD checks finish.
    stage([Check("fea", ROOT / "fea", "run_fea.py", (), ROOT / "fea/results.json")], False)
    stage([
        Check("body_layout", BODY, "check_body_layout.py", (), BODY / "generated/body-layout-checks.json"),
        Check("yaw_stage", BODY, "check_yaw_stage.py", (), BODY / "generated/yaw-stage.json"),
    ])
    return summary(results)


def summary(results):
    print(f"{'check':<16} {'result':<12} {'seconds':>9}  detail")
    print("-" * 76)
    for name, status, elapsed, detail, _ in results:
        print(f"{name:<16} {status:<12} {elapsed:9.1f}  {detail}")
    return int(any(status not in ("pass", "cached") for _, status, _, _, _ in results))


if __name__ == "__main__":
    raise SystemExit(main())
