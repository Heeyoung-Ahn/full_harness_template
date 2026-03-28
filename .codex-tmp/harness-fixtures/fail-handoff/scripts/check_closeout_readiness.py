from __future__ import annotations

import argparse

from harness_utils import (
    CURRENT_STATE_PATH,
    TASK_LIST_PATH,
    count_handoff_entries,
    extract_bullet_value,
    extract_section,
    file_line_count,
    load_artifact,
    parse_active_locks,
    parse_task_rows,
    print_failures,
    section_is_effectively_empty,
    has_live_blockers,
    template_mode_enabled,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices={"day_wrap_up", "version_closeout"}, required=True)
    args = parser.parse_args()

    current_meta, current_body = load_artifact(CURRENT_STATE_PATH)
    task_meta, task_body = load_artifact(TASK_LIST_PATH)

    if template_mode_enabled(current_meta, task_meta):
        print(f"[SKIP] check_closeout_readiness ({args.mode}): template_mode=true detected.")
        return 0

    failures: list[str] = []

    if parse_active_locks(task_body):
        failures.append("TASK_LIST.md still has active locks. Clear or explicitly resolve them before closeout.")

    if current_meta.get("task_list_sync_check") != "In Sync":
        failures.append("CURRENT_STATE.md must be marked 'In Sync' before closeout.")

    if not current_meta.get("sync_checked_at"):
        failures.append("CURRENT_STATE.md sync_checked_at must be filled in before closeout.")

    if count_handoff_entries(task_body) > 8:
        failures.append("TASK_LIST.md still exceeds the handoff entry limit. Compact history before closeout.")

    if file_line_count(TASK_LIST_PATH) > 220:
        failures.append("TASK_LIST.md still exceeds the 220-line cap. Compact history before closeout.")

    latest_handoff_summary = extract_section(current_body, "Latest Handoff Summary")
    if count_handoff_entries(task_body) > 0 and section_is_effectively_empty(latest_handoff_summary):
        failures.append("CURRENT_STATE.md must summarize the latest handoff before closeout.")

    if args.mode == "version_closeout":
        blockers_section = extract_section(task_body, "Blockers")
        if has_live_blockers(blockers_section):
            failures.append("TASK_LIST.md still has live blockers. Version closeout requires a resolved blocker list.")

        needs_user_decision = extract_bullet_value(current_body, "Needs User Decision")
        if needs_user_decision and needs_user_decision.lower() not in {"없음", "none", "n/a"}:
            failures.append("CURRENT_STATE.md still has 'Needs User Decision'. Resolve it before version closeout.")

        review_or_release_tasks = [
            row
            for row in parse_task_rows(task_body)
            if row["task_id"].startswith(("REV-", "REL-")) and row["state"] != "x"
        ]
        if review_or_release_tasks:
            failures.append("Review and release tasks must be completed before version closeout.")

    return print_failures(f"check_closeout_readiness ({args.mode})", failures)


if __name__ == "__main__":
    raise SystemExit(main())

