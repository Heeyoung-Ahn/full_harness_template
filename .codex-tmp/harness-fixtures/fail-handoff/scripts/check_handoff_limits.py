from __future__ import annotations

from harness_utils import (
    CURRENT_STATE_PATH,
    TASK_LIST_PATH,
    count_handoff_entries,
    count_in_progress_tasks,
    extract_section,
    file_line_count,
    load_artifact,
    print_failures,
    section_is_effectively_empty,
)


def main() -> int:
    current_meta, current_body = load_artifact(CURRENT_STATE_PATH)
    task_meta, task_body = load_artifact(TASK_LIST_PATH)

    failures: list[str] = []

    actual_handoff_count = count_handoff_entries(task_body)
    actual_active_task_count = count_in_progress_tasks(task_body)
    actual_line_count = file_line_count(TASK_LIST_PATH)

    if task_meta.get("handoff_entry_count") != actual_handoff_count:
        failures.append(
            "TASK_LIST.md frontmatter handoff_entry_count must match the number of entries in '## Handoff Log'."
        )

    if task_meta.get("active_task_count") != actual_active_task_count:
        failures.append("TASK_LIST.md frontmatter active_task_count must match the number of in-progress tasks.")

    if actual_handoff_count > 8:
        failures.append("TASK_LIST.md must keep at most 8 recent handoff entries.")

    if actual_line_count > 220:
        failures.append("TASK_LIST.md must stay at or below 220 lines.")

    if (actual_handoff_count > 8 or actual_line_count > 220) and not task_meta.get("last_compacted_at"):
        failures.append("TASK_LIST.md must update last_compacted_at when handoff compaction is required.")

    latest_handoff_summary = extract_section(current_body, "Latest Handoff Summary")
    if actual_handoff_count > 0 and section_is_effectively_empty(latest_handoff_summary):
        failures.append("CURRENT_STATE.md must summarize the latest handoff when TASK_LIST.md has handoff entries.")

    return print_failures("check_handoff_limits", failures)


if __name__ == "__main__":
    raise SystemExit(main())
