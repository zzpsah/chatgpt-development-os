# Operating Principles

## 1. Human-first interface
The user describes outcomes, problems, ideas, or goals in ordinary language. Internal routing is invisible unless useful to explain the work.

## 2. Inspect before changing
For existing software, inspect the relevant repository, configuration, database schema, and documentation before making non-trivial changes.

## 3. Evidence over assumption
Use repository files, tests, database metadata, official documentation, and other reliable sources when available. Label assumptions.

## 4. Progressive depth
Do not perform a heavyweight process for a trivial task. Increase analysis, testing, and review effort with risk and complexity.

## 5. Persistent state
Important project facts, decisions, milestones, and blockers belong in durable project files rather than only in chat history.

## 6. Small reversible changes
Prefer focused commits and reviewable changes. Avoid unrelated cleanup during feature work.

## 7. Verification is part of implementation
A change is not complete until appropriate tests or validation have been performed, or the limitation is explicitly reported.

## 8. Security by default
Protect secrets and sensitive information. Apply least privilege, input validation, authorization checks, and safe file handling where relevant.
