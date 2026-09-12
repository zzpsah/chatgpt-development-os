# DevOS Repository Identity Contract

## Purpose

This file is the canonical identity boundary for the Development OS repository itself. A human may call the system `DEVOS`, `Development OS`, or `ChatGPT Development OS`, but repository resolution must use the canonical repository identity below.

## Canonical identity

- **Project name:** ChatGPT Development OS
- **Project ID:** `chatgpt-development-os`
- **Canonical repository:** `zzpsah/chatgpt-development-os`
- **Owner:** `zzpsah`
- **Default branch:** `main`
- **Visibility:** public
- **DevOS aliases:** `DEVOS`, `Development OS`, `ChatGPT Development OS`

## Resolution rule

When a user says `DEVOS` while working on this system, an AI must first resolve the repository through repository-local evidence. The canonical repository is `zzpsah/chatgpt-development-os`.

A repository with a similar name is not an acceptable substitute merely because GitHub search returns it first. In particular, `SamyPesse/devos` is an unrelated external repository and must never be treated as this project.

## Fresh-session bootstrap

A fresh AI session should establish identity in this order:

1. Read root `AGENTS.md`.
2. Read `core/ai-bootstrap-protocol.md`.
3. Read `.ai/manifest.yaml`.
4. Read `.ai/repository-identity.json`.
5. Verify the actual Git/repository target before material changes.
6. Only then recover `.ai/CURRENT-STATE.md`, tasks, decisions, architecture, and recent history.

## Non-authority rule

This identity contract resolves **which repository DevOS refers to**. It does not grant execution, write, deployment, production, merge, or authorization authority. Existing controller, authorization, security, verification, and runtime gates remain authoritative.

## Conflict handling

If the connected GitHub account cannot access the canonical repository, or repository metadata contradicts this contract, report `REPOSITORY_IDENTITY_UNCONFIRMED` and stop material work until the conflict is resolved. Never silently substitute another repository.
