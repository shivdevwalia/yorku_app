# Manager handoff

## State and boundaries

[Issue #3](https://github.com/shivdevwalia/yorku_app/issues/3) prepares the approved [product baseline](product-plan.md) and [roadmap](milestone-roadmap.md). Python backend mandatory; frontend Next.js/TypeScript. Documentation awaiting merge/review: inspect actual PR status, never assume merge. Mutable head/PR/T3 identifiers belong in implementation return/PR, not a guessed future head here.

Verified starting SHA: `cd9db8eb9e8d3ece367ce8cc29058bd4513c8b5d`; implementation branch `t3/yorku-planning-docs`; draft PR target `main`. No dependency work bundled.

Today: documentation/templates and `assets/icon.svg`; no app dependencies/toolchain, build command, tests, or configured CI validation. No app tests or production extraction run for this task.

Approved: product baseline and documentation preparation. Not authorized: milestone-0 execution, scraping/data collection, app code, dependencies, deployment, extra milestone issues, merge. Final explicit approval precedes merge/deployment; draft PR is review handoff only.

Access/scraping authorization is context for future work, not execution permission here. Redistribution/retention/display and third-party rights separately unverified. No verified production feed/parser; daily refresh provisional. EECS/MATH plus connected subjects candidates, not fixed pilot.

## Next manager

1. Read [AGENTS.md](../AGENTS.md), [workflow](development-workflow.md), product plan, roadmap. Inspect status, exact branch/base/head, open issues/PRs, active T3 work before edits/dispatch.
2. Resolve documentation review/merge status accurately; arrange exact-SHA independent review as needed and request final merge approval. Baseline approval is not execution approval.
3. Request explicit milestone-0 authorization. Until granted, do not fetch datasets, scrape, implement, install dependencies, create extra milestone issues, deploy.
4. Once authorized, execute only approved source/rights inventory, representative rules/data audit, feasibility/pilot selection. Record unresolved rights, refresh evidence, go/no-go. Request next-scope approval at exit, not blanket multi-milestone authorization.

## Coordination and validation

One manager per milestone owns decomposition, dependencies, integration, handoff. Record GitHub issue/PR URLs, T3 task/thread IDs, branch, exact base/head, dependencies, scope, acceptance, evidence in briefs/PRs as available. Issue #3 covers documentation; no extra milestone issues now.

Future authorized workers use `delegate_task`, `isolation: worktree`, never shell worktrees. Verify starting SHA; mismatch blocks. Max two independent implementers, data and UI/domain only after contracts. Serialize overlap/dependencies. No worker subdelegation unless authorized. Follow completion events/returned next instructions, not polling.

Each independent review round gets a new reviewer with exact SHA/base/acceptance/evidence brief. Manager resolves findings, integrates in dependency order. Reviewer returns findings, SHA, actual validation/limitations. Older-SHA reviews do not cover newer changes. Final handoff records PR/head/base/checks/reviews/risks and requests explicit merge/deployment approval.

Documentation validation: local Markdown/HTML links relative to containing files, including templates; `git diff --check`; scope/consistency review. Do not install toolchains or invent tests. References do not prove rights/extraction; record external availability not verified.

When app exists: frontend type/lint/build; Python lint/type/domain; ingestion fixture regression; OpenAPI-generated/validated contract compatibility; integration. Stable required checks later. Quality: traceable sources, unknown handling, feasible schedules, no-solution/limit explanations, student usefulness, phone/keyboard, reproducible/versioned results.

## Copyable opening prompt

```text
Act as parent manager for the next authorized York academic planner milestone.
Read AGENTS.md, docs/development-workflow.md, docs/product-plan.md,
docs/milestone-roadmap.md, docs/manager-handoff.md. Inspect repository status,
exact branch/base/head, open issues/PRs including #3, documentation review/merge
state, active T3 work. Do not assume the documentation PR merged.
Baseline requires Python authoritative deterministic planning/ingestion,
Next.js/TypeScript frontend, versioned API contracts. No app toolchain/tests yet.
No chatbot, paid LLM dependency, Passport York handling, automatic enrolment.
Baseline/documentation approval did not authorize milestone 0. Request explicit
authorization for source/rights inventory, representative data/rules audit,
feasibility/pilot choice before execution. EECS/MATH plus connected subjects are
candidates only. Access does not prove redistribution/retention/display or
third-party rights. Until authorized do not scrape, fetch datasets, implement,
install dependencies, create extra milestone issues, deploy.
Use one manager, max two independent implementers after contracts, T3-managed
isolated worktrees, completion events not polling, new exact-SHA reviewers.
Require final explicit merge/deployment approval. Report state and the specific
authorization needed next.
```
