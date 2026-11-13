# Manager handoff

## State and boundaries

[Issue #3](https://github.com/shivdevwalia/yorku_app/issues/3) prepares the approved [product baseline](product-plan.md) and [roadmap](milestone-roadmap.md). Python backend mandatory; frontend Next.js/TypeScript. Inspect issue #3 and its linked PR for current documentation review/merge status; do not reopen completed review or approval work. Mutable head/PR/T3 identifiers belong in implementation return/PR, not a guessed future head here.

Milestone-0 verified starting SHA: `7d3c7a4455d620e8277237eed73280e576a7e589`, merged baseline [PR #4](https://github.com/shivdevwalia/yorku_app/pull/4), issue #3 closed. Implementation branch: `t3/milestone-zero-research-audit`; draft PR target `main`. See [milestone-0 audit](milestone-0/README.md); exact final head/PR belong in implementation return/PR.

Today: documentation/templates and `assets/icon.svg`; no app dependencies/toolchain, build command, tests, or configured CI validation. No app tests or production extraction run for this task.

At baseline approval, authorized scope was product baseline and documentation preparation. That approval did not authorize: milestone-0 execution, scraping/data collection, app code, dependencies, deployment, extra milestone issues, merge. Final explicit approval precedes merge/deployment; draft PR is review handoff only.

On November 13, 2026 the user explicitly authorized milestone-0 documentation/research under [issue #5](https://github.com/shivdevwalia/yorku_app/issues/5): small representative public-source inspection, rights inventory and feasibility/pilot recommendation. No bulk extraction, authentication, app code or dependencies. Milestone 1 is NOT authorized. Rights remain unresolved; no verified feed/parser or live section bundles. Audit proposes a conditional eight-course catalog review set; public replicated catalog and verified scheduling remain no-go.

## Subsequent collection authorization and correction

On November 13, 2026 the user explicitly attested full authorization to scrape/obtain York data and instructed collection to proceed. Bounded public-source collection is authorized; do not ask again or treat access-permission uncertainty as a research blocker. No access-control bypass or private records. Downstream retention/redistribution/public-display/third-party rights are not independently verified; milestone-1 app implementation, dependencies, merge and deployment remain separate approval boundaries.

Read the [audit follow-up correction](milestone-0/README.md#authorization-and-follow-up-correction): /cds is enrolled Class Schedule View, not proof public course search requires login. Anonymous public pages expose Winter 2027 catalogue identifiers; current section/component/meeting data remains technically unverified. Prior no-collection instructions below refer to initial scope and are superseded by this authorization. The original PR head passed independent review without blocking findings; later changes are not covered by that exact-SHA review.

## Next manager

1. Read [AGENTS.md](../AGENTS.md), [workflow](development-workflow.md), product plan, roadmap. Inspect status, exact branch/base/head, open issues/PRs, active T3 work before edits/dispatch.
2. Check issue #3 and its linked PR. If already merged, continue without repeating completed review/approval. If open, resolve remaining findings and obtain final merge approval. Baseline approval is not execution approval.
3. Milestone-0 research authorization is recorded; do not request it again. Independently review audit and exact draft head, resolve findings and obtain explicit merge approval.
4. Request decisions on rights ownership, conditional pilot and next scope at research exit. Milestone 1 needs separate authorization; do not implement, install dependencies, bulk extract or deploy.

## Coordination and validation

One manager per milestone owns decomposition, dependencies, integration, handoff. Record GitHub issue/PR URLs, T3 task/thread IDs, branch, exact base/head, dependencies, scope, acceptance, evidence in briefs/PRs as available. Issue #3 covered baseline documentation; #5 covers milestone-0 research. No later milestone issues authorized here.

Future authorized workers use `delegate_task`, `isolation: worktree`, never shell worktrees. Verify starting SHA; mismatch blocks. Max two independent implementers, data and UI/domain only after contracts. Serialize overlap/dependencies. No worker subdelegation unless authorized. Follow completion events/returned next instructions, not polling.

Each independent review round gets a new reviewer with exact SHA/base/acceptance/evidence brief. Manager resolves findings, integrates in dependency order. Reviewer returns findings, SHA, actual validation/limitations. Older-SHA reviews do not cover newer changes. Final handoff records PR/head/base/checks/reviews/risks and requests explicit merge/deployment approval.

Documentation validation: local Markdown/HTML links relative to containing files, including templates; `git diff --check`; scope/consistency review. Do not install toolchains or invent tests. Audit records observed external availability/failures, not rights clearance or extraction reliability.

When app exists: frontend type/lint/build; Python lint/type/domain; ingestion fixture regression; OpenAPI-generated/validated contract compatibility; integration. Stable required checks later. Quality: traceable sources, unknown handling, feasible schedules, no-solution/limit explanations, student usefulness, phone/keyboard, reproducible/versioned results.

## Copyable opening prompt

```text
Act as parent manager for the next authorized York academic planner milestone.
Read AGENTS.md, docs/development-workflow.md, docs/product-plan.md,
docs/milestone-roadmap.md, docs/manager-handoff.md. Inspect repository status,
exact branch/base/head, open issues/PRs including #5, research review/merge
state, active T3 work. Baseline PR #4 merged and issue #3 closed.
Baseline requires Python authoritative deterministic planning/ingestion,
Next.js/TypeScript frontend, versioned API contracts. No app toolchain/tests yet.
No chatbot, paid LLM dependency, Passport York handling, automatic enrolment.
Milestone-0 documentation/research was authorized November 13, 2026 in #5.
Read docs/milestone-0/README.md and review its exact implementation head.
Eight-course review set is conditional, not validated coverage. Access does not
prove redistribution/retention/display or third-party rights. Milestone 1 is not
authorized. Request next-scope approval at exit; do not bulk extract,
authenticate, implement, install dependencies or deploy.
Use one manager, max two independent implementers after contracts, T3-managed
isolated worktrees, completion events not polling, new exact-SHA reviewers.
Require final explicit merge/deployment approval. Report state and the specific
authorization needed next.
```
