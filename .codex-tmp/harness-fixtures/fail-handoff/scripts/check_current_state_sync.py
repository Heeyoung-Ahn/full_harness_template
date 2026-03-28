from __future__ import annotations

from harness_utils import (
    ARCHITECTURE_PATH,
    CURRENT_STATE_PATH,
    IMPLEMENTATION_PLAN_PATH,
    REQUIREMENTS_PATH,
    TASK_LIST_PATH,
    extract_bullet_value,
    load_artifact,
    parse_active_locks,
    print_failures,
    template_mode_enabled,
)


def main() -> int:
    current_meta, current_body = load_artifact(CURRENT_STATE_PATH)
    requirements_meta, _ = load_artifact(REQUIREMENTS_PATH)
    architecture_meta, _ = load_artifact(ARCHITECTURE_PATH)
    plan_meta, _ = load_artifact(IMPLEMENTATION_PLAN_PATH)
    task_meta, task_body = load_artifact(TASK_LIST_PATH)

    if template_mode_enabled(current_meta, requirements_meta, architecture_meta, plan_meta, task_meta):
        print("[SKIP] check_current_state_sync: template_mode=true detected. Initialize a real project first.")
        return 0

    failures: list[str] = []

    expected_status_pairs = [
        ("requirements_status", requirements_meta.get("status"), "Requirements Status"),
        ("architecture_status", architecture_meta.get("status"), "Architecture Status"),
        ("plan_status", plan_meta.get("status"), "Plan Status"),
    ]

    for frontmatter_key, expected_value, bullet_label in expected_status_pairs:
        frontmatter_value = current_meta.get(frontmatter_key)
        bullet_value = extract_bullet_value(current_body, bullet_label)
        if frontmatter_value != expected_value:
            failures.append(
                f"CURRENT_STATE.md frontmatter {frontmatter_key!r} must match source artifact status {expected_value!r}."
            )
        if not bullet_value:
            failures.append(f"CURRENT_STATE.md bullet '{bullet_label}' must be filled in.")
        elif bullet_value != frontmatter_value:
            failures.append(
                f"CURRENT_STATE.md bullet '{bullet_label}' must match frontmatter value {frontmatter_value!r}."
            )

    sync_checked_at = current_meta.get("sync_checked_at", "")
    if not sync_checked_at:
        failures.append("CURRENT_STATE.md frontmatter sync_checked_at must not be empty.")

    body_sync_checked_at = extract_bullet_value(current_body, "Sync Checked At")
    if not body_sync_checked_at:
        failures.append("CURRENT_STATE.md bullet 'Sync Checked At' must be filled in.")
    elif body_sync_checked_at != sync_checked_at:
        failures.append("CURRENT_STATE.md bullet 'Sync Checked At' must match frontmatter sync_checked_at.")

    sync_check_value = current_meta.get("task_list_sync_check")
    if sync_check_value != "In Sync":
        failures.append("CURRENT_STATE.md frontmatter task_list_sync_check must be 'In Sync' before handoff.")

    body_sync_check = extract_bullet_value(current_body, "Task List Sync Check")
    if not body_sync_check:
        failures.append("CURRENT_STATE.md bullet 'Task List Sync Check' must be filled in.")
    elif body_sync_check != sync_check_value:
        failures.append("CURRENT_STATE.md bullet 'Task List Sync Check' must match frontmatter task_list_sync_check.")

    if current_meta.get("next_agent") in {"", "TBD"}:
        failures.append("CURRENT_STATE.md frontmatter next_agent must name the next real role.")

    recommended_role = extract_bullet_value(current_body, "Recommended role")
    if not recommended_role:
        failures.append("CURRENT_STATE.md bullet 'Recommended role' must be filled in.")
    elif recommended_role != current_meta.get("next_agent"):
        failures.append("CURRENT_STATE.md bullet 'Recommended role' must match frontmatter next_agent.")

    active_locks = parse_active_locks(task_body)
    current_locks_to_respect = extract_bullet_value(current_body, "Current locks to respect")
    active_task_ids = extract_bullet_value(current_body, "Active Task IDs")

    if active_locks and not current_locks_to_respect:
        failures.append("CURRENT_STATE.md must list current locks when TASK_LIST.md has active locks.")
    if active_locks and not active_task_ids:
        failures.append("CURRENT_STATE.md must list active task IDs when TASK_LIST.md has active locks.")

    for lock in active_locks:
        task_id = lock["task_id"]
        if task_id not in current_body:
            failures.append(f"CURRENT_STATE.md must reference active lock task {task_id}.")

    return print_failures("check_current_state_sync", failures)


if __name__ == "__main__":
    raise SystemExit(main())
