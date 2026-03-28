# Project Start Checklist

이 문서는 **템플릿 저장소를 실제 프로젝트로 전환할 때** 바로 따라 하는 실행용 체크리스트입니다.

- 규칙 정본은 여전히 [.agents/rules/workspace.md](.agents/rules/workspace.md)입니다.
- 설명이 더 필요하면 [PROJECT_WORKFLOW_MANUAL.md](PROJECT_WORKFLOW_MANUAL.md)를 읽습니다.
- 이 문서의 목적은 `template_mode: true` 상태의 템플릿을 `template_mode: false` 상태의 실제 프로젝트로 안전하게 넘기는 것입니다.

## 1. 시작 전 확인

- [ ] 이 저장소를 더 이상 배포용 템플릿 그대로 유지할 필요가 없다.
- [ ] 실제 사용자 요청이나 실제 프로젝트 목표가 있다.
- [ ] 첫 작업 역할은 Planner로 시작한다.
- [ ] 일반 터미널에서 Python 실행이 가능하다.

Python 확인:

```powershell
& "C:\Users\ahyne\AppData\Local\Programs\Python\Launcher\py.exe" --version
```

짧게 되면:

```powershell
py --version
```

## 2. 가장 먼저 읽을 문서

순서는 항상 아래와 같습니다.

1. [AGENTS.md](AGENTS.md)
2. [.agents/rules/workspace.md](.agents/rules/workspace.md)
3. [.agents/artifacts/CURRENT_STATE.md](.agents/artifacts/CURRENT_STATE.md)
4. [.agents/artifacts/TASK_LIST.md](.agents/artifacts/TASK_LIST.md)의 `## Active Locks`
5. `CURRENT_STATE.md > Must Read Next`

## 3. `template_mode` 전환 대상

아래 5개 문서의 frontmatter만 먼저 바꿉니다.

- [CURRENT_STATE.md](.agents/artifacts/CURRENT_STATE.md)
- [REQUIREMENTS.md](.agents/artifacts/REQUIREMENTS.md)
- [ARCHITECTURE_GUIDE.md](.agents/artifacts/ARCHITECTURE_GUIDE.md)
- [IMPLEMENTATION_PLAN.md](.agents/artifacts/IMPLEMENTATION_PLAN.md)
- [TASK_LIST.md](.agents/artifacts/TASK_LIST.md)

모두 공통으로:

- [ ] `template_mode: true`를 `template_mode: false`로 바꾼다.

중요:

- 처음부터 모든 문서를 완성할 필요는 없습니다.
- 하지만 `template_mode: false`로 바꾸는 순간부터는 validator가 실제 프로젝트 문서로 간주합니다.
- 그래서 최소한 frontmatter와 기본 상태값은 실제 값으로 채워야 합니다.

## 4. 첫 상태값 넣기

### `REQUIREMENTS.md`

- [ ] `status: Draft` 또는 `Needs User Answers`로 설정
- [ ] `approved_by`, `approved_at`는 아직 비워도 됨

### `ARCHITECTURE_GUIDE.md`

- [ ] `status: Draft`로 설정
- [ ] `approved_by`, `approved_at`는 아직 비워도 됨

### `IMPLEMENTATION_PLAN.md`

- [ ] `status: Draft`로 설정
- [ ] `current_iteration`에 임시 값이라도 넣기
  - 예: `Iteration 1`
- [ ] `validation_commands_status`는 실제 명령이 없으면 `missing`

### `CURRENT_STATE.md`

- [ ] `next_agent: Planner`
- [ ] `requirements_status`는 `REQUIREMENTS.md`와 같게 맞춤
- [ ] `architecture_status`는 `ARCHITECTURE_GUIDE.md`와 같게 맞춤
- [ ] `plan_status`는 `IMPLEMENTATION_PLAN.md`와 같게 맞춤
- [ ] `sync_checked_at`에 현재 시각 입력
- [ ] `task_list_sync_check`는 처음 정렬이 끝났으면 `In Sync`, 아직 어긋나면 `Needs Review`

### `TASK_LIST.md`

- [ ] `active_task_count: 0`
- [ ] `handoff_entry_count: 0`
- [ ] `last_compacted_at: ""`

## 5. 본문에서 바로 채워야 하는 최소 항목

`template_mode: false` 직후 최소한 아래는 비워 두지 않는 편이 안전합니다.

### `CURRENT_STATE.md`

- [ ] `Snapshot`
- [ ] `Next Recommended Agent`
- [ ] `Must Read Next`
- [ ] `Active Scope`
- [ ] `Open Decisions / Blockers`

권장 초기값:

- `Recommended role: Planner`
- `Reason: Real project bootstrap in progress.`
- `Trigger to switch: Requirements draft completed.`

### `REQUIREMENTS.md`

- [ ] `Quick Read`
- [ ] `Product Goal`
- [ ] `In Scope`
- [ ] `Out of Scope`
- [ ] `Open Questions`

### `ARCHITECTURE_GUIDE.md`

- [ ] `Quick Read`
- [ ] `Approved Boundaries`
- [ ] `Forbidden Changes`

### `IMPLEMENTATION_PLAN.md`

- [ ] `Quick Read`
- [ ] `Current Iteration`
- [ ] `Validation Commands`

### `TASK_LIST.md`

- [ ] 현재 프로젝트에 맞는 첫 Planner task 추가
- [ ] DEV/TST/REV 예시 placeholder는 실제 프로젝트 시작 전에 교체하거나 삭제
- [ ] 개발/테스트/리뷰 task에는 반드시 `Scope`를 적기

## 6. 첫 검증 명령

### 부트스트랩 직후

이 단계에서는 strict gate가 아직 다 통과할 필요는 없습니다.

```powershell
& "C:\Users\ahyne\AppData\Local\Programs\Python\Launcher\py.exe" scripts\check_artifact_schema.py
```

기대 결과:

- [ ] `check_artifact_schema`는 PASS
- [ ] planner gate는 아직 실패할 수 있음

### Planner 문서를 다듬는 동안

```powershell
& "C:\Users\ahyne\AppData\Local\Programs\Python\Launcher\py.exe" scripts\check_planner_gate.py
```

기대 결과:

- 요구사항, 아키텍처, 구현 계획이 덜 닫혀 있으면 FAIL
- 이 FAIL은 정상입니다. 아직 Developer로 넘길 준비가 안 됐다는 뜻입니다.

### Developer handoff 직전

```powershell
& "C:\Users\ahyne\AppData\Local\Programs\Python\Launcher\py.exe" scripts\run_harness_checks.py --phase planner
& "C:\Users\ahyne\AppData\Local\Programs\Python\Launcher\py.exe" scripts\run_harness_checks.py --phase handoff
```

기대 결과:

- [ ] 둘 다 PASS일 때만 Developer handoff

## 7. Planner가 Developer로 넘기기 전에 꼭 만족해야 하는 것

- [ ] `REQUIREMENTS.md` frontmatter `status: Approved`
- [ ] `ARCHITECTURE_GUIDE.md` frontmatter `status: Approved`
- [ ] `IMPLEMENTATION_PLAN.md` frontmatter `status: Ready for Execution`
- [ ] `CURRENT_STATE.md`의 상태값이 위 3문서와 일치
- [ ] `TASK_LIST.md`의 DEV/TST/REV task에 `Scope`가 있다
- [ ] placeholder가 남아 있지 않다
- [ ] `scripts\check_planner_gate.py` PASS
- [ ] `scripts\check_current_state_sync.py` PASS
- [ ] `scripts\check_handoff_limits.py` PASS

## 8. 실패해도 정상인 것과 비정상인 것

### 정상

- 프로젝트 시작 직후 `check_planner_gate.py` FAIL
- requirements 초안 단계에서 `status: Draft`
- open questions가 남아 있는 상태

### 비정상

- `template_mode: false`인데 `check_artifact_schema.py` FAIL
- `CURRENT_STATE.md` 상태와 실제 문서 상태가 다름
- `TASK_LIST.md`에 Scope 없는 DEV/TST/REV task가 있음
- placeholder를 남긴 채 Developer handoff 시도

## 9. 아주 짧은 시작 순서

1. `AGENTS.md` 읽기
2. `workspace.md` 읽기
3. `CURRENT_STATE.md`와 `TASK_LIST.md > ## Active Locks` 확인
4. 핵심 5개 artifact를 `template_mode: false`로 전환
5. 첫 상태값 입력
6. `check_artifact_schema.py` 실행
7. Planner가 요구사항/아키텍처/계획 작성
8. `run_harness_checks.py --phase planner`
9. `run_harness_checks.py --phase handoff`
10. PASS면 Developer handoff

## 10. 추천 시작 문구

실제 첫 요청을 받을 때 Planner가 이렇게 시작하면 됩니다.

```text
이 저장소를 실제 프로젝트 모드로 전환합니다.
먼저 requirements, architecture, implementation plan의 초안을 만들고,
핵심 artifact의 template_mode를 false로 바꾼 뒤 schema 검사를 통과시키겠습니다.
```
