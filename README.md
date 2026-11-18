<img src="assets/icon.svg" width="64" height="64" alt="">

# YorkU_App

Created in [T3 Code](https://t3.codes).

Start development by reading [AGENTS.md](AGENTS.md) and the [development workflow](docs/development-workflow.md). Create a task with the [issue template](.github/ISSUE_TEMPLATE/task.md), including acceptance criteria, scope, dependencies, and validation. The parent manager dispatches self-contained briefs to T3-managed isolated workers and arranges independent review.

Use the [PR template](.github/pull_request_template.md) to return the exact commit and validation evidence. Final explicit user approval is required before merge or deployment.

The local Lassonde course explorer and prerequisite reference map now have a Python API and Next.js/TypeScript frontend. See [setup, sources and limitations](docs/lassonde-build.md). Run `python -m backend.ingest`, then `python -m backend.server`; in another terminal run `cd frontend`, `npm ci`, and `npm run dev`. No installation is needed for documentation-only work.

Implementation is tracked in [issue #7](https://github.com/shivdevwalia/yorku_app/issues/7). The app uses official-source local data, not the separate fictional `prototype/index.html`. It is not an authoritative eligibility or degree audit. No public deployment is authorized.

## Academic planner baseline

- [Product plan](docs/product-plan.md)
- [Milestone roadmap](docs/milestone-roadmap.md)
- [Manager handoff](docs/manager-handoff.md)

Baseline [PR #4](https://github.com/shivdevwalia/yorku_app/pull/4) merged and issue #3 closed. User authorized documentation/research milestone 0 on November 13, 2026 under [issue #5](https://github.com/shivdevwalia/yorku_app/issues/5); see the [audit and conditional pilot recommendation](docs/milestone-0/README.md). The later local Lassonde map/search scope is authorized under issue #7; broader roadmap milestones remain gated. Final explicit approval still precedes merge/deployment.
