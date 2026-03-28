# Full Harness Standalone Template

이 폴더는 `full_harness`를 독립 템플릿처럼 바로 복제해서 쓰기 위한 최소 운영 세트입니다.

## 무엇이 들어 있나
- `AGENTS.md`: 모든 AI의 진입 인덱스
- `.agents/`: rule, workflow, skill, artifact 정본
- `scripts/`: harness validator
- `.github/`: CI에서 validator를 돌리는 예시
- `PROJECT_START_CHECKLIST.md`: 템플릿을 실제 프로젝트로 전환하는 체크리스트
- `PROJECT_WORKFLOW_MANUAL.md`: 사람용 설명서

## 바로 복제해서 쓰는 절차
1. `full_harness` 폴더를 통째로 복사하거나, 안의 파일들을 새 프로젝트 루트에 복제합니다.
2. 새 폴더 이름을 프로젝트 이름에 맞게 바꿉니다.
3. Codex에서 복제한 그 폴더 자체를 workspace root로 엽니다.
4. 새 프로젝트에 기존 코드가 없다면 그대로 시작합니다. 기존 코드베이스에 붙일 때는 이 폴더의 파일들을 기존 프로젝트 루트에 합칩니다.
5. 가장 먼저 `AGENTS.md`를 읽고, 이어서 `.agents/rules/workspace.md`, `.agents/artifacts/CURRENT_STATE.md`, `.agents/artifacts/TASK_LIST.md > ## Active Locks` 순서로 들어갑니다.
6. `CURRENT_STATE.md`가 아직 template bootstrap 상태라면 바로 `PROJECT_START_CHECKLIST.md`를 따라 `template_mode: true` 상태를 `template_mode: false` 상태로 전환합니다.
7. Planner가 요구사항, 아키텍처, 구현 계획 초안을 채운 뒤 validator를 실행합니다.

## 첫 실행 명령
기본 예시는 `python` 기준입니다. Windows에서 `python`이 잡히지 않으면 `py` 또는 로컬 interpreter 경로로 같은 명령을 실행합니다.

```powershell
python scripts\check_artifact_schema.py
python scripts\run_harness_checks.py --phase planner
python scripts\run_harness_checks.py --phase handoff
```

## 복제할 때 주의할 점
- 상위 폴더를 열지 말고, 복제한 폴더 자체를 루트로 엽니다.
- 상대 경로는 현재 폴더 기준으로 맞춰져 있습니다.
- 이 템플릿의 기본 운영 모델은 `Codex main agent + Codex sub-agent + 필요 시 git worktree`입니다.
- `PROJECT_WORKFLOW_MANUAL.md`는 설명서이지 기본 진입 문서가 아닙니다.
- `template_mode: true` 상태에서는 strict validator가 일부 `SKIP`되는 것이 정상입니다.
