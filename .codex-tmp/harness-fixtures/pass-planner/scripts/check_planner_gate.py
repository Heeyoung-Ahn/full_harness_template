from __future__ import annotations

from harness_utils import (
    ARCHITECTURE_PATH,
    CURRENT_STATE_PATH,
    IMPLEMENTATION_PLAN_PATH,
    REQUIREMENTS_PATH,
    TASK_LIST_PATH,
    contains_placeholders,
    extract_section,
    has_noncomment_command,
    load_artifact,
    parse_markdown_table,
    parse_task_rows,
    print_failures,
    section_is_effectively_empty,
    template_mode_enabled,
)


def main() -> int:
    requirements_meta, requirements_body = load_artifact(REQUIREMENTS_PATH)
    architecture_meta, architecture_body = load_artifact(ARCHITECTURE_PATH)
    plan_meta, plan_body = load_artifact(IMPLEMENTATION_PLAN_PATH)
    task_meta, task_body = load_artifact(TASK_LIST_PATH)
    current_state_meta, current_state_body = load_artifact(CURRENT_STATE_PATH)

    if template_mode_enabled(
        requirements_meta,
        architecture_meta,
        plan_meta,
        task_meta,
        current_state_meta,
    ):
        print("[SKIP] check_planner_gate: template_mode=true detected. Initialize a real project first.")
        return 0

    failures: list[str] = []

    if requirements_meta.get("status") != "Approved":
        failures.append("REQUIREMENTS.md frontmatter status must be 'Approved'.")
    if architecture_meta.get("status") != "Approved":
        failures.append("ARCHITECTURE_GUIDE.md frontmatter status must be 'Approved'.")
    if plan_meta.get("status") != "Ready for Execution":
        failures.append("IMPLEMENTATION_PLAN.md frontmatter status must be 'Ready for Execution'.")

    for title in ("In Scope", "Out of Scope", "Open Questions"):
        section = extract_section(requirements_body, title)
        if section_is_effectively_empty(section):
            failures.append(f"REQUIREMENTS.md section {title!r} must not be empty.")

    for title in ("Approved Boundaries", "Forbidden Changes"):
        section = extract_section(architecture_body, title)
        if section_is_effectively_empty(section):
            failures.append(f"ARCHITECTURE_GUIDE.md section {title!r} must not be empty.")

    current_iteration = extract_section(plan_body, "Current Iteration")
    if section_is_effectively_empty(current_iteration):
        failures.append("IMPLEMENTATION_PLAN.md section 'Current Iteration' must not be empty.")

    validation_commands = extract_section(plan_body, "Validation Commands")
    if not has_noncomment_command(validation_commands):
        failures.append("IMPLEMENTATION_PLAN.md section 'Validation Commands' must contain runnable commands.")

    functional_rows = parse_markdown_table(extract_section(requirements_body, "Functional Requirements"))
    if not functional_rows:
        failures.append("REQUIREMENTS.md must contain at least one functional requirement row.")
    else:
        for index, row in enumerate(functional_rows, start=1):
            if len(row) < 4 or not row[3].strip():
                failures.append(f"REQUIREMENTS.md functional requirement row {index} is missing Acceptance Criteria.")

    nonfunctional_rows = parse_markdown_table(extract_section(requirements_body, "Non-Functional Requirements"))
    if not nonfunctional_rows:
        failures.append("REQUIREMENTS.md must contain at least one non-functional requirement row.")
    else:
        for index, row in enumerate(nonfunctional_rows, start=1):
            if len(row) < 4 or not row[3].strip():
                failures.append(
                    f"REQUIREMENTS.md non-functional requirement row {index} is missing Acceptance Criteria."
                )

    domain_rows = parse_markdown_table(extract_section(architecture_body, "Domain Map"))
    if not domain_rows:
        failures.append("ARCHITECTURE_GUIDE.md must contain at least one domain map row.")

    task_rows = [
        row
        for row in parse_task_rows(task_body)
        if row["task_id"].startswith(("DEV-", "TST-", "REV-")) and row["state"] != "x"
    ]
    if not task_rows:
        failures.append("TASK_LIST.md must contain executable DEV/TST/REV rows before Developer handoff.")
    else:
        for row in task_rows:
            if not row["scope"].strip():
                failures.append(f"TASK_LIST.md row {row['task_id']} is missing Scope.")

    for path_name, text in (
        ("REQUIREMENTS.md", requirements_body),
        ("ARCHITECTURE_GUIDE.md", architecture_body),
        ("IMPLEMENTATION_PLAN.md", plan_body),
        ("TASK_LIST.md", task_body),
        ("CURRENT_STATE.md", current_state_body),
    ):
        placeholder_hits = contains_placeholders(text)
        if placeholder_hits:
            failures.append(f"{path_name} still contains placeholder markers: {', '.join(sorted(set(placeholder_hits)))}.")

    if current_state_meta.get("next_agent") in {"", "TBD"}:
        failures.append("CURRENT_STATE.md frontmatter next_agent must point to the next real role before handoff.")

    return print_failures("check_planner_gate", failures)


if __name__ == "__main__":
    raise SystemExit(main())
