from __future__ import annotations

from pathlib import Path
import re
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = ROOT_DIR / ".agents" / "artifacts"

CURRENT_STATE_PATH = ARTIFACTS_DIR / "CURRENT_STATE.md"
REQUIREMENTS_PATH = ARTIFACTS_DIR / "REQUIREMENTS.md"
ARCHITECTURE_PATH = ARTIFACTS_DIR / "ARCHITECTURE_GUIDE.md"
IMPLEMENTATION_PLAN_PATH = ARTIFACTS_DIR / "IMPLEMENTATION_PLAN.md"
TASK_LIST_PATH = ARTIFACTS_DIR / "TASK_LIST.md"
HANDOFF_ARCHIVE_PATH = ARTIFACTS_DIR / "HANDOFF_ARCHIVE.md"


REQUIREMENTS_STATUSES = {
    "Draft",
    "Needs User Answers",
    "Ready for Approval",
    "Approved",
}
ARCHITECTURE_STATUSES = {
    "Draft",
    "Ready for Approval",
    "Approved",
}
PLAN_STATUSES = {
    "Draft",
    "Ready for Execution",
}
TASK_LIST_SYNC_VALUES = {
    "In Sync",
    "Needs Review",
}


ARTIFACT_SPECS: dict[Path, dict[str, Any]] = {
    CURRENT_STATE_PATH: {
        "kind": "CURRENT_STATE",
        "required_frontmatter": {
            "artifact_kind",
            "template_mode",
            "next_agent",
            "requirements_status",
            "architecture_status",
            "plan_status",
            "sync_checked_at",
            "task_list_sync_check",
        },
        "enum_fields": {
            "requirements_status": REQUIREMENTS_STATUSES,
            "architecture_status": ARCHITECTURE_STATUSES,
            "plan_status": PLAN_STATUSES,
            "task_list_sync_check": TASK_LIST_SYNC_VALUES,
        },
        "required_headings": {
            "Maintenance Rules",
            "Snapshot",
            "Next Recommended Agent",
            "Must Read Next",
            "Active Scope",
            "Task Pointers",
            "Open Decisions / Blockers",
            "Latest Handoff Summary",
            "Recent History Summary",
        },
    },
    REQUIREMENTS_PATH: {
        "kind": "REQUIREMENTS",
        "required_frontmatter": {
            "artifact_kind",
            "template_mode",
            "status",
            "approved_by",
            "approved_at",
        },
        "enum_fields": {
            "status": REQUIREMENTS_STATUSES,
        },
        "required_headings": {
            "Quick Read",
            "Status",
            "Open Questions",
            "Product Goal",
            "In Scope",
            "Out of Scope",
            "Functional Requirements",
            "Non-Functional Requirements",
            "Approval History",
        },
    },
    ARCHITECTURE_PATH: {
        "kind": "ARCHITECTURE_GUIDE",
        "required_frontmatter": {
            "artifact_kind",
            "template_mode",
            "status",
            "approved_by",
            "approved_at",
        },
        "enum_fields": {
            "status": ARCHITECTURE_STATUSES,
        },
        "required_headings": {
            "Quick Read",
            "Status",
            "Approved Boundaries",
            "Forbidden Changes",
            "Architecture Summary",
            "Domain Map",
            "Change Control",
        },
    },
    IMPLEMENTATION_PLAN_PATH: {
        "kind": "IMPLEMENTATION_PLAN",
        "required_frontmatter": {
            "artifact_kind",
            "template_mode",
            "status",
            "current_iteration",
            "validation_commands_status",
        },
        "enum_fields": {
            "status": PLAN_STATUSES,
            "validation_commands_status": {"missing", "present"},
        },
        "required_headings": {
            "Quick Read",
            "Status",
            "Current Iteration",
            "Validation Commands",
            "Stage Plan",
            "Iteration Plan",
            "Handoff Notes",
        },
    },
    TASK_LIST_PATH: {
        "kind": "TASK_LIST",
        "required_frontmatter": {
            "artifact_kind",
            "template_mode",
            "active_task_count",
            "handoff_entry_count",
            "last_compacted_at",
        },
        "required_headings": {
            "Changelog",
            "Usage Rules",
            "Current Release Target",
            "Active Locks",
            "Blockers",
            "Handoff Log",
        },
    },
}


PLACEHOLDER_PATTERNS = [
    re.compile(r"\[YYYY-MM-DD HH:MM\]"),
    re.compile(r"\[User\]"),
    re.compile(r"\[요구사항\]"),
    re.compile(r"\[기능/도메인 범위 작성\]"),
    re.compile(r"\[어떤 상태가 되면 충족인지\]"),
    re.compile(r"\[폴더/모듈/문서\]"),
    re.compile(r"\[개발 작업\]"),
    re.compile(r"\[검증 작업\]"),
    re.compile(r"\[대상 Task ID / 경로 / 요구사항\]"),
    re.compile(r"\[릴리즈 범위 / 대상 Task ID\]"),
    re.compile(r"\[환경 / 버전 / 커밋 범위\]"),
    re.compile(r"\[환경 / 명령 / 배포 대상\]"),
    re.compile(r"\[제품/문서/기술 부채\]"),
    re.compile(r"\[설명\]"),
    re.compile(r"\[영향\]"),
    re.compile(r"\[대응\]"),
    re.compile(r"\[역할\]"),
    re.compile(r"\[Task ID\]"),
    re.compile(r"\[DomainA\]"),
    re.compile(r"\[DomainB\]"),
    re.compile(r"TBD"),
]


TASK_LINE_RE = re.compile(
    r"^- \[(?P<state>[ x!\-])\]\s+(?P<task_id>[A-Z]+-\d+)\s+(?P<title>.*?)\s+(?:—|-)\s+Scope:\s+(?P<scope>.+)$"
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return {}, text

    try:
        end_index = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("Unterminated frontmatter block") from exc

    frontmatter: dict[str, Any] = {}
    for raw_line in lines[1:end_index]:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")
        key, raw_value = line.split(":", 1)
        frontmatter[key.strip()] = parse_scalar(raw_value.strip())

    body = "\n".join(lines[end_index + 1 :])
    return frontmatter, body


def parse_scalar(value: str) -> Any:
    if value in {"''", '""'}:
        return ""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def load_artifact(path: Path) -> tuple[dict[str, Any], str]:
    return parse_frontmatter(read_text(path))


def extract_headings(body: str) -> set[str]:
    headings: set[str] = set()
    for line in body.splitlines():
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            headings.add(match.group(2).strip())
    return headings


def extract_section(body: str, heading: str) -> str:
    lines = body.splitlines()
    start_index: int | None = None
    heading_level = 0

    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match and match.group(2).strip() == heading:
            start_index = index + 1
            heading_level = len(match.group(1))
            break

    if start_index is None:
        return ""

    end_index = len(lines)
    for index in range(start_index, len(lines)):
        match = re.match(r"^(#{1,6})\s+(.*)$", lines[index])
        if match and len(match.group(1)) <= heading_level:
            end_index = index
            break

    return "\n".join(lines[start_index:end_index]).strip()


def extract_bullet_value(body: str, label: str) -> str:
    pattern = re.compile(rf"^- {re.escape(label)}:\s*(.*)$", re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    return match.group(1).strip()


def parse_markdown_table(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and all(re.fullmatch(r"[:\- ]+", cell) for cell in cells):
            continue
        rows.append(cells)

    if len(rows) <= 1:
        return []
    return rows[1:]


def parse_task_rows(body: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in body.splitlines():
        match = TASK_LINE_RE.match(line.strip())
        if match:
            rows.append(match.groupdict())
    return rows


def parse_active_locks(body: str) -> list[dict[str, str]]:
    rows = parse_markdown_table(extract_section(body, "Active Locks"))
    parsed_rows: list[dict[str, str]] = []
    for row in rows:
        if len(row) >= 9:
            parsed_rows.append(
                {
                    "task_id": row[0],
                    "agent": row[1],
                    "role": row[2],
                    "session": row[3],
                    "branch": row[4],
                    "worktree": row[5],
                    "started_at": row[6],
                    "scope": row[7],
                    "note": row[8],
                }
            )
            continue
        if len(row) < 6:
            continue
        parsed_rows.append(
            {
                "task_id": row[0],
                "agent": row[1],
                "role": row[2],
                "session": "",
                "branch": "",
                "worktree": "",
                "started_at": row[3],
                "scope": row[4],
                "note": row[5],
            }
        )
    return [row for row in parsed_rows if any(value.strip() for value in row.values())]


def count_handoff_entries(body: str) -> int:
    return len(re.findall(r"^###\s+", extract_section(body, "Handoff Log"), re.MULTILINE))


def count_in_progress_tasks(body: str) -> int:
    return sum(1 for row in parse_task_rows(body) if row["state"] == "-")


def file_line_count(path: Path) -> int:
    return len(read_text(path).splitlines())


def contains_placeholders(text: str) -> list[str]:
    found: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            found.append(pattern.pattern)
    return found


def section_is_effectively_empty(section: str) -> bool:
    meaningful_lines: list[str] = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("```"):
            continue
        if line.startswith("|---"):
            continue
        meaningful_lines.append(line)
    return not meaningful_lines


def has_noncomment_command(section: str) -> bool:
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("```") or line.startswith("#"):
            continue
        return True
    return False


def has_live_blockers(section: str) -> bool:
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "없으면 비워" in line:
            continue
        if "[없음]" in line:
            continue
        if "[없으면 비워둠]" in line:
            continue
        if "Needs User Decision" in line:
            return True
        if line.startswith("- "):
            return True
    return False


def template_mode_enabled(*frontmatters: dict[str, Any]) -> bool:
    return any(bool(frontmatter.get("template_mode")) for frontmatter in frontmatters)


def print_failures(script_name: str, failures: list[str]) -> int:
    if not failures:
        print(f"[PASS] {script_name}")
        return 0

    print(f"[FAIL] {script_name}")
    for failure in failures:
        print(f"- {failure}")
    return 1


