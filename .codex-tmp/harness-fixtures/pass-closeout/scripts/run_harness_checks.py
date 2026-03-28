from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


SCRIPTS_DIR = Path(__file__).resolve().parent


def run_script(script_name: str, *extra_args: str) -> int:
    command = [sys.executable, str(SCRIPTS_DIR / script_name), *extra_args]
    print(f"[RUN] {' '.join(command)}")
    result = subprocess.run(command, check=False)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase",
        choices={"planner", "handoff", "closeout", "all"},
        default="all",
    )
    parser.add_argument(
        "--mode",
        choices={"day_wrap_up", "version_closeout"},
        default="day_wrap_up",
    )
    args = parser.parse_args()

    scripts: list[tuple[str, tuple[str, ...]]] = []

    if args.phase in {"planner", "all"}:
        scripts.extend(
            [
                ("check_artifact_schema.py", ()),
                ("check_planner_gate.py", ()),
            ]
        )

    if args.phase in {"handoff", "all"}:
        scripts.extend(
            [
                ("check_artifact_schema.py", ()),
                ("check_current_state_sync.py", ()),
                ("check_handoff_limits.py", ()),
            ]
        )

    if args.phase in {"closeout", "all"}:
        scripts.extend(
            [
                ("check_artifact_schema.py", ()),
                ("check_current_state_sync.py", ()),
                ("check_handoff_limits.py", ()),
                ("check_closeout_readiness.py", ("--mode", args.mode)),
            ]
        )

    seen: set[tuple[str, tuple[str, ...]]] = set()
    ordered_scripts: list[tuple[str, tuple[str, ...]]] = []
    for item in scripts:
        if item in seen:
            continue
        seen.add(item)
        ordered_scripts.append(item)

    exit_code = 0
    for script_name, extra_args in ordered_scripts:
        script_exit_code = run_script(script_name, *extra_args)
        if script_exit_code != 0:
            exit_code = script_exit_code
            break

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
