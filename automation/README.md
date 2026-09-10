# Development OS Automatic Project Discovery

The Development OS is designed to eliminate routine project-context setup.

## Design

A resident worker watches approved project roots on a local machine and automatically:

1. detects likely software projects;
2. creates the project-local `.ai/` context if missing;
3. preserves any existing `.ai/` files;
4. analyzes repository metadata and common manifests;
5. records only evidence-backed project facts;
6. detects meaningful development events for later context synchronization.

GitHub repositories can use repository-side automation to validate that a project has a portable context. The local worker is required for truly automatic detection of arbitrary local folders because GitHub and cloud ChatGPT cannot watch a user's local filesystem continuously.

## Safety

The worker must never create `.ai/` in every arbitrary directory. It uses project markers and configured roots. It must never copy secrets into context. It should prefer creating context over modifying source code.

## Account independence

Project context belongs to the project. It must not depend on a ChatGPT, GitHub, Claude, or other AI account. Moving a repository or changing AI tools must preserve `.ai/`.
