from __future__ import annotations

import sys

from harness_utils import ARTIFACT_SPECS, extract_headings, load_artifact, print_failures


def main() -> int:
    failures: list[str] = []

    for path, spec in ARTIFACT_SPECS.items():
        frontmatter, body = load_artifact(path)

        if not frontmatter:
            failures.append(f"{path.name}: frontmatter is missing.")
            continue

        expected_kind = spec["kind"]
        actual_kind = frontmatter.get("artifact_kind")
        if actual_kind != expected_kind:
            failures.append(
                f"{path.name}: artifact_kind must be {expected_kind!r}, found {actual_kind!r}."
            )

        for key in sorted(spec["required_frontmatter"]):
            if key not in frontmatter:
                failures.append(f"{path.name}: frontmatter key {key!r} is missing.")

        for key, allowed_values in spec.get("enum_fields", {}).items():
            if key in frontmatter and frontmatter[key] not in allowed_values:
                failures.append(
                    f"{path.name}: frontmatter {key!r} must be one of {sorted(allowed_values)}, "
                    f"found {frontmatter[key]!r}."
                )

        headings = extract_headings(body)
        missing_headings = sorted(spec["required_headings"] - headings)
        for heading in missing_headings:
            failures.append(f"{path.name}: required heading {heading!r} is missing.")

    return print_failures("check_artifact_schema", failures)


if __name__ == "__main__":
    raise SystemExit(main())
