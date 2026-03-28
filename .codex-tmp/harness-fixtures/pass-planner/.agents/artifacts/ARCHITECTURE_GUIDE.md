---
artifact_kind: ARCHITECTURE_GUIDE
template_mode: false
status: Approved
approved_by: User
approved_at: "2026-03-28 21:05"
---

# Architecture Guide

## Quick Read
- 현재 확인된 아키텍처 상태: 문서 중심 예시 구조
- 도메인 경계: Example domain only
- 이번 범위에서 건드리는 폴더/모듈: `src/example/*`
- 상태와 데이터의 주인: example domain
- 다음 역할이 꼭 지켜야 할 구조 규칙: presentation -> application -> domain
- 이번 문서의 리뷰 승인자: User

## Status
- Document Status: Approved
- Owner: Planner
- Last Updated At: 2026-03-28 21:05
- Last Approved By: User
- Last Approved At: 2026-03-28 21:05

## Approved Boundaries
- 도메인 경계: example domain is isolated from auth and deploy concerns.
- 계층 책임 경계: presentation triggers application, application coordinates domain, domain owns core rules.
- 확인된 예외: 없음

## Forbidden Changes
- 확인 없이 추가하면 안 되는 레이어/파일: auth, billing, deployment modules
- 금지되는 직접 참조: presentation -> infrastructure direct business logic calls
- 금지되는 구조 우회: bypassing application services

## Changelog
- [2026-03-28] Planner: approved architecture guide

## Architecture Summary
- 아키텍처 스타일: layered modular structure
- 주요 도메인: example
- 도메인 간 상호작용: none in this scope

## Domain Map

| Domain | Responsibility | Key Entities / Use Cases | Notes |
|---|---|---|---|
| Example | Execute the example flow | ExampleAction, ExampleResult | Single-scope validation domain |

## Folder Structure
```text
src/
  example/
    application/
    domain/
    infrastructure/
    presentation/
```

## Layer Responsibilities
- `domain/`: example rules and entities
- `application/`: example use-case orchestration
- `infrastructure/`: adapters if needed
- `presentation/`: entry points and UI wiring

## Dependency Rules
- domain does not import application/presentation/infrastructure.
- application depends on domain abstractions.
- infrastructure implements application/domain contracts.
- presentation calls application services only.

## State and Data Ownership
- 전역 상태: 없음
- 로컬 UI 상태: presentation local state only
- 영속 저장소: 없음
- 캐시 전략: 없음

## Integration Boundaries
- 외부 API/서비스: 없음
- 인증 경계: 없음
- 파일/스토리지 경계: 문서 파일만 사용

## Naming Conventions
- 모듈: example*
- 파일: feature-oriented names
- 이벤트/함수: verb-first naming
- 상태/액션: explicit status names

## Change Control
- 구조 변경이 필요하면 Planner가 이유와 영향 범위를 기록한다.
- 사용자 확인 전에는 본 문서를 수정하지 않는다.
