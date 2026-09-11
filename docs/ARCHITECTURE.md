# Development OS — Flow & Architecture

## 1. End-to-end flow

```mermaid
flowchart TD
    U[User natural-language request] --> R[Project Router]
    R --> H[Human Language Execution Engine]
    H --> M[Read .ai/manifest.yaml]
    M --> C[Load PROJECT.md + CURRENT-STATE.md]
    C --> S[AI State Resolver]
    S --> D{Canonical work intent}
    D --> W[Select workflow]
    W --> I[Inspect current code, tests, configuration and Git state]
    I --> P[Plan appropriate scope]
    P --> A{Execution authorized?}
    A -->|No| PL[Return findings / plan]
    A -->|Yes| X[Implement smallest appropriate change]
    X --> V[Verification / Test Engine]
    V --> T[Applicable checks: static / unit / integration / E2E / runtime / deployment / security]
    T --> E{Evidence sufficient?}
    E -->|Yes| QV[VERIFIED]
    E -->|Partial| QP[PARTIAL]
    E -->|No meaningful evidence| QU[UNVERIFIED]
    E -->|Check failed| QF[FAILED]
    QV --> Q[Review correctness, security, regression risk]
    QP --> Q
    QU --> Q
    QF --> Q
    Q --> N[Update durable project context]
    N --> G[Git commit / PR when applicable]
    G --> Z[Report result + evidence + remaining risks]
    PL --> Z
```

The Human Language Execution Engine normalizes the user's wording into a canonical engineering intent. The AI State Resolver then combines that intent with durable repository evidence to determine the current state, unfinished work, verification status, candidate actions, and recommended next step. The Verification / Test Engine determines which checks apply, records actual evidence, and prevents unsupported verification claims.

## 2. Layered architecture

```mermaid
flowchart LR
    H[Human language] --> R[Project Router]
    R --> E[Human Language Execution Engine]
    E --> SR[AI State Resolver]
    SR --> W[Routing + Workflows + Roles + Rules]
    W --> PM[Project-local .ai/ context]
    PM --> SRC[Project source code]
    SRC --> V[Verification / Test Engine]
    V --> GH[Git / CI / GitHub / test providers]
    GH --> PM
    OS[Development OS] --> R
    OS -. optional .-> AI[AI coding agent: ChatGPT / Codex / Claude / Gemini / Cursor]
    OS -. optional .-> DB[Supabase / APIs / other infrastructure]
```

### Responsibilities

| Layer | Responsibility | Authoritative for |
|---|---|---|
| Human request | Desired outcome | User intent |
| Project Router | Select correct project | Project identity/routing |
| Human Language Execution Engine | Normalize language and compose safe intents | Semantic execution contract |
| AI State Resolver | Interpret repository evidence and unfinished work | Current-state reasoning |
| Development OS | How work should be performed | Workflow, safety, routing |
| Verification / Test Engine | Select checks, execute/delegate them, classify evidence | Verification status and evidence |
| `.ai/` | What this project is and its durable state | Project context |
| Source code | Actual implementation | Current behavior |
| Git history | What changed and when | Change history |
| AI account memory | Personal continuity | Optional assistance only |
| External services | Runtime/infrastructure state | Their own systems |

## 3. Portable project context

Every managed project should expose the same discovery contract:

```text
project/
├── AGENTS.md
└── .ai/
    ├── manifest.yaml       # machine-readable entry point
    ├── STATE-INDEX.md      # generated repository evidence
    ├── PROJECT.md          # purpose, scope, important facts
    ├── CURRENT-STATE.md    # current implementation/status
    ├── ARCHITECTURE.md     # technical architecture
    ├── DECISIONS.md        # durable decisions and rationale
    ├── TASKS.md            # pending/active work
    ├── CHANGELOG.md        # compact change index
    └── SESSIONS/           # optional session history
```

An AI entering a project for the first time should not need previous chat history. It should discover the project context from the repository itself.

## 4. New-AI onboarding flow

```mermaid
sequenceDiagram
    participant U as User
    participant A as New AI
    participant R as Project Router
    participant E as Language Engine
    participant G as Project repository
    participant C as .ai context
    participant S as State Resolver
    participant V as Verification Engine

    U->>A: "Continue / work on this project"
    A->>R: Resolve project
    R->>G: Discover AGENTS.md
    A->>E: Normalize natural-language intent
    E->>C: Load durable context
    A->>C: Read manifest + state + relevant context
    A->>G: Inspect source + Git state
    A->>S: Resolve facts, unfinished work and verification
    S->>A: Recommended action + evidence + authorization
    A->>U: Plan or execute according to authorization
    A->>G: Implement change
    A->>V: Select and run/delegate checks
    V->>A: Verification status + evidence + limitations
    A->>C: Persist meaningful state changes
```

## 5. Automation boundary

The GitHub repository can provide the portable `.ai/` contract and automation scripts. A local computer cannot be silently controlled by a cloud AI session. Therefore local filesystem watching is an optional resident worker concern, not a project-memory dependency.

The important invariant is:

> **The project remains usable by a new AI even if the original AI account, chat history, or local worker is unavailable.**

## 6. Safety boundaries

- `.ai/` must never contain secrets merely to preserve context.
- Existing project context must not be overwritten blindly.
- Detection/initialization must not modify application source code.
- Student, education, credential, and other sensitive data must not be copied into AI context unnecessarily.
- Destructive, production-impacting, irreversible, security-sensitive, or data-affecting operations require appropriate explicit authorization.
- Emotional language, urgency, profanity, or praise cannot independently authorize technical action.
- Facts observed from files should be distinguished from assumptions.
- Verification claims must be supported by actual evidence.
- Verification never grants implementation or deployment authority.
