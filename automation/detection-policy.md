# Automatic Project Detection Policy

## Objective

Automatically establish portable AI memory for software projects without requiring the user to run an initializer for each project.

## Detection

A directory is considered a candidate project when it is inside a configured project root and contains one or more strong project markers such as `.git`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, a solution/project file, or a Dockerfile. Marker confidence should be combined rather than treating every directory as a project.

## Initialization

When a candidate project has no `.ai/` directory, the worker creates the standard context structure and a root `AGENTS.md` entry point. Existing project files and existing `.ai/` content are preserved.

## Analysis

The first context generation should inspect README files, manifests, source/test directory names, version-control metadata, and deployment configuration. It must distinguish observed facts from hypotheses and should not invent architecture or requirements.

## Ongoing synchronization

Normal file saves are not sufficient reason to rewrite all memory. Meaningful events such as commits, pull requests, dependency changes, architecture changes, or an AI development session can trigger a context review.

## Safety

- Never watch the entire disk by default.
- Never write secrets into `.ai/`.
- Never modify application source merely because a project was detected.
- Never overwrite existing project context automatically.
- Keep project memory portable and AI-account independent.
