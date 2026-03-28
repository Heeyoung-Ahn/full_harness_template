---
artifact_kind: ARCHITECTURE_GUIDE
template_mode: false
status: Draft
approved_by: ""
approved_at: ""
---

# Architecture Guide

> ??臾몄꽌??DDD-first 援ъ“ 怨꾩빟?쒖엯?덈떎.  
> Developer, Tester, Reviewer, DevOps????臾몄꽌瑜?湲곗??쇰줈 ?묒뾽?섎ŉ, ?꾩쓽 援ъ“ 蹂寃쎌? 湲덉??⑸땲??

## Quick Read
- ?꾩옱 ?뱀씤???꾪궎?띿쿂 ?ㅽ???
- ?듭떖 ?꾨찓??寃쎄퀎:
- ?대쾲 踰붿쐞?먯꽌 嫄대뱶由щ뒗 ?대뜑/紐⑤뱢:
- ?곹깭? ?곗씠?곗쓽 二쇱씤:
- ?ㅼ쓬 ??븷??瑗?吏耳쒖빞 ??援ъ“ 洹쒖튃:
- ?대쾲 臾몄꽌??由щ럭 ?ъ씤??

## Status
- Document Status: Draft / Ready for Approval / Approved
- Owner: Planner
- Last Updated At: [YYYY-MM-DD HH:MM]
- Last Approved By: [User]
- Last Approved At: [YYYY-MM-DD HH:MM]

## Approved Boundaries
- ?꾨찓??寃쎄퀎:
- 怨꾩링 梨낆엫 寃쎄퀎:
- ?뱀씤???덉쇅:

## Forbidden Changes
- ?뱀씤 ?놁씠 異붽??섎㈃ ???섎뒗 ?대뜑/?덉씠??
- 湲덉???吏곸젒 李몄“:
- 湲덉???援ъ“ ?고쉶:

## Changelog
- [YYYY-MM-DD] Planner: initial draft

## Architecture Summary
- ?꾪궎?띿쿂 ?ㅽ???
- 二쇱슂 ?꾨찓??
- ?듭떖 ?ㅺ퀎 ?먯튃:

## Domain Map

| Domain | Responsibility | Key Entities / Use Cases | Notes |
|---|---|---|---|
| [DomainA] | [梨낆엫] | [?듭떖 媛쒕뀗] | [硫붾え] |
| [DomainB] | [梨낆엫] | [?듭떖 媛쒕뀗] | [硫붾え] |

## Folder Structure
```text
src/
  [domain-a]/
    application/
    domain/
    infrastructure/
    presentation/
  [domain-b]/
    application/
    domain/
    infrastructure/
    presentation/
```

## Layer Responsibilities
- `domain/`: ?뷀떚?? 媛?媛앹껜, ?꾨찓??洹쒖튃
- `application/`: ?좎뒪耳?댁뒪, ?ㅼ??ㅽ듃?덉씠?? ?쒕퉬???명꽣?섏씠??- `infrastructure/`: ?몃? API, DB, ?뚯씪?쒖뒪?? ?ㅽ듃?뚰겕 援ы쁽
- `presentation/`: UI, route, controller, screen, component

## Dependency Rules
- domain? application/presentation/infrastructure瑜?紐⑤Ⅸ??
- application? domain???ъ슜?섎ŉ, 援ъ껜 援ы쁽蹂대떎 異붿긽 怨꾩빟???섏〈?쒕떎.
- infrastructure??application/domain 怨꾩빟??援ы쁽?쒕떎.
- presentation? application???몄텧?섍퀬, 吏곸젒 鍮꾩쫰?덉뒪 洹쒖튃??媛吏吏 ?딅뒗??

## State and Data Ownership
- ?꾩뿭 ?곹깭:
- 濡쒖뺄 UI ?곹깭:
- ?곸냽 ??μ냼:
- 罹먯떆 ?꾨왂:

## Integration Boundaries
- ?몃? API/?쒕퉬??
- ?몄쬆 寃쎄퀎:
- ?뚯씪/?ㅽ넗由ъ? 寃쎄퀎:

## Naming Conventions
- ?대뜑:
- ?뚯씪:
- ?대옒???⑥닔:
- ?곹깭/?≪뀡:

## Change Control
- 援ъ“ 蹂寃쎌씠 ?꾩슂?섎㈃ Planner媛 ?댁쑀? ?곹뼢 踰붿쐞瑜?湲곕줉?쒕떎.
- ?ъ슜???뱀씤 ?꾩뿉留???臾몄꽌瑜??섏젙?쒕떎.

