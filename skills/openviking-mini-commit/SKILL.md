---
name: openviking-mini-commit
description: Prepare and commit openviking-mini changes. Use before staging or committing code in this repository to enforce documentation-first work, scoped diffs, passing or clearly reported tests, clean staging, and concise commit messages.
---

# openviking-mini Commit Skill

Use this skill before creating a commit in `openviking-mini`.

## Commit Preconditions

1. Read `AGENTS.md`.
2. Inspect `git status --short`.
3. Inspect the diff for every file that will be staged.
4. Confirm the change is about the OpenViking mini-core or its project constraints.
5. Confirm docs, interfaces, and tests are present when runtime behavior changed.
6. Run the tester skill or record why tests cannot run.

## Staging Rules

- Stage only files related to the current task.
- Do not stage unrelated user changes.
- Do not stage generated artifacts unless they are required source files.
- Review staged diff before committing.

## Commit Message Rules

Use a short imperative subject:

```text
Add project testing and commit skills
```

Prefer one concise body paragraph only when it explains a non-obvious decision.

## Final Checks

Before committing, verify:

- `git diff --cached` matches the intended scope.
- Tests passed, or the limitation is explicitly documented.
- The commit does not include secrets, local paths with credentials, build outputs, or unrelated files.
- The final response names the commit hash if a commit was created.

## Stop Conditions

Stop and ask before committing if:

- The working tree contains unrelated modified tracked files.
- Tests fail for reasons unrelated to the current task.
- The staged diff includes files outside the intended scope.
- The requested commit would violate `AGENTS.md`.
