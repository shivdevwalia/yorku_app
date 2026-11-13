# Development workflow

## Roles and task tracking

The parent manager decomposes work, chooses bases, records dependencies, integrates changes, and requests final user approval. Implementation workers own their assigned changes and validation. An independent reviewer checks the exact proposed commit against the acceptance criteria and reports actionable findings.

Use GitHub issues for goals and acceptance criteria, PRs for changes and review evidence, and T3 task/thread IDs for execution. Record the issue link, T3 ID, base, dependencies, branch, head SHA, and PR link in the brief or PR as they become available. Use ordinary issue/PR checklists for status; do not add a custom tracking database. Never record secrets.

## Dispatch a self-contained brief

Copy and fill this format so a child needs no prior conversation:

```text
Goal and GitHub issue URL:
Acceptance criteria:
Allowed scope and excluded work:
Repository and working environment:
Base remote/branch or exact required local commit:
Dependencies (issue/PR/T3 IDs, required commits, readiness):
T3 task/thread ID (record after dispatch):
Implementation constraints and relevant repository instructions:
Validation commands and expected evidence:
Deliverables (files, commit SHA, branch, PR URL, limitations):
Approval boundary (no merge or deployment without final user approval):
```

Dispatch implementation with `delegate_task`, `isolation: "worktree"`. Let T3 prepare the checkout; do not create worktrees in shell commands or in the child's task. Children do all assigned work themselves and do not subdelegate unless explicitly authorized. Initially allow at most two implementation workers at once, and only when their changes are independent.

## Dependencies and bases

`delegate_task` with `isolation: "worktree"` starts from the parent's current commit. It has no `baseRef` parameter, and uncommitted edits are excluded. A base named in a brief does not select the checkout base.

Before each implementation dispatch:

1. Choose the required base. For independent work, fetch origin and resolve `origin/main` to an exact SHA. Honor an explicitly requested base. Without a remote, resolve the local default branch. For dependent work, first wait for the prerequisite result, verify its commit is available locally, and resolve that required branch or commit to an exact SHA.
2. Inspect the parent checkout with `git status --short`, `git branch --show-current`, and `git rev-parse HEAD`. Require a clean checkout and no other agent actively editing that checkout before switching it. Preserve user changes; never reset, clean, or silently stash them to prepare a task.
3. If HEAD differs from the required SHA, align the parent checkout with `git switch --detach <required-SHA>` only when that clean, idle checkout can safely be switched. Record its original branch/HEAD first. If switching would interfere with user work or the manager's T3 workspace binding, stop dispatch and resolve that workspace constraint explicitly; do not claim the brief changes the base.
4. Verify `git rev-parse HEAD` equals the required SHA, then call `delegate_task` with `isolation: "worktree"`. Require the worker's first action to compare its starting `git rev-parse HEAD` with the expected SHA before making edits. A mismatch blocks implementation and must be reported to the manager.
5. After T3 has prepared the child checkout, restore any temporary parent checkout change to the recorded branch/HEAD, provided it is still clean and idle. Record the actual child starting SHA, dependency, branch, and final SHA in the result/PR.

Serialize overlapping or dependent edits by default, and integrate in dependency order. Keep each branch scoped to its issue. If a base changes, revalidate the resulting head before handoff.

`t3_thread_launch` accepts `workspaceStrategy.baseRef`, but creates an independent top-level thread rather than a delegated child. Use it only when the user explicitly requests a new thread; it is not a workaround for ordinary worker delegation. Never create worker worktrees in the shell or ask a child to create its own checkout.

## Completion and independent review

Follow T3 completion notifications and the returned `next` instructions. Do not repeatedly poll delegate status, use sleep loops, or create watchers to detect completion. On completion, the manager checks the returned commit, evidence, and limitations before integration.

Start each independent review round with a new `delegate_task` and a self-contained review brief naming the issue, PR, exact head SHA, base, acceptance criteria, and validation expectations. Do not reuse an old delegate conversation for a new review round. Reviewers return:

```text
Reviewed head SHA and base:
Acceptance criteria assessed:
Findings (severity, file/line, impact, required fix), or no findings:
Validation actually run and results:
Checks not run and limitations:
Recommendation and required follow-up:
```

After fixes, record the new SHA and obtain a new independent review when needed. A review of an older SHA is not evidence for later changes. The manager prepares the final handoff with the PR link, exact SHA, checks/review state, remaining risks, and an explicit request for final user approval before merge or deployment. Never infer approval from a successful check or draft PR creation.

## Setup and validation today

The repository currently contains documentation/templates and `assets/icon.svg`. There is no application toolchain, dependency manifest, build command, test suite, or CI validation configured. No dependency installation is needed. Do not invent build/test commands or claim they passed.

For documentation changes:

1. Read the linked issue and [repository instructions](../AGENTS.md).
2. Check every local Markdown/HTML link against its path relative to the containing file. Check template links as well.
3. Run `git diff --check` before committing and inspect `git diff` for scope and consistency across the instructions, guide, and templates.
4. Record the commands, results, exact commit, and any unperformed checks in the PR. Independent review remains separate from implementation validation.

## GitHub CLI on Windows and authentication

If `gh` is not on PATH, invoke the installed executable with PowerShell's call operator:

```powershell
& 'C:/Program Files/GitHub CLI/gh.exe' --version
```

Use existing secure GitHub authentication. If persistent `gh` login fails because `read:org` is missing, do not repeatedly log in or request broader credentials merely for repository operations. When an existing Git credential is authorized, retrieve it privately using `git credential fill`, parse its password into process-local `GH_TOKEN`, and invoke `gh` by its absolute path in the same process. Remove `GH_TOKEN` afterward in a `finally` block. Never print credential output, enable command tracing around it, persist the token, or put credentials in command arguments, files, issue bodies, PRs, or briefs. Do not run credential retrieval where raw output is captured in logs.

If PR creation is denied, report the permission failure and the pushed branch/commit for handoff; do not ask for tokens. Open the PR as a draft with the issue-closing reference and accurate validation evidence. Link the created PR to T3 immediately using `link_pull_request`. Merge and deployment still require final explicit user approval.
