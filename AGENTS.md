# Repository workflow

- The parent manager owns decomposition, dependencies, integration, and the user handoff. Track work with T3 task/thread IDs and GitHub issue/PR links.
- Run at most two implementation workers concurrently, only for independent changes. Serialize overlapping or dependent changes by default.
- Start workers with `delegate_task` and `isolation: "worktree"`; never create worker worktrees in a shell. Workers must not subdelegate unless explicitly authorized.
- Give each child a self-contained brief: goal, acceptance criteria, scope, repository/base, dependencies, validation, and expected return. See [the workflow](docs/development-workflow.md).
- Follow completion notifications and returned `next` instructions instead of polling delegates. Each new independent review round uses a new `delegate_task`.
- Workers implement and validate their assigned scope. Reviewers independently inspect the exact commit and report findings, SHA, and validation evidence. The manager resolves findings and integrates in dependency order.
- Final explicit user approval is required before merging or deployment. A draft PR is a review handoff, not approval.
- This repository has no application dependencies, build command, or tests. Do not invent test results or install a toolchain for documentation work. Never include secrets in files, logs, briefs, or PRs.
