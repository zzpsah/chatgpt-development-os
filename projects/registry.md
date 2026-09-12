# Project Registry

This registry maps natural-language project names to their durable repositories and repository-local portable context.

| Project | Repository | Context | Notes |
|---|---|---|---|
| DevOS / Development OS | `zzpsah/chatgpt-development-os` | `.ai/PROJECT.md` | Canonical DevOS framework repository; canonical alias `DEVOS`; exact owner/repository wins over name-only search |
| UMV Tetahali | `zzpsah/umv-tetahali` | target repo `.ai/PROJECT.md` | Production/project repository; DevOS portable memory + automatic context sync enabled |
| UMV Tetahali Staging | `zzpsah/umv-tetahali-staging` | target repo `.ai/PROJECT.md` | Staging repository; existing project docs preserved; DevOS automatic context sync enabled |
| UMV Sahaspur | `zzpsah/umvsahaspur` | target repo `.ai/PROJECT.md` | School project; current application tree was empty at onboarding; DevOS automatic context sync enabled |
| Photo Signature Studio | `zzpsah/photo-signature-studio` | target repo `.ai/PROJECT.md` | Image/photo workflow; existing knowledge base preserved; DevOS automatic context sync enabled |
| Automation Suite | `zzpsah/automation-suite` | target repo `.ai/PROJECT.md` | Multiple automation modules; repository-level DevOS memory + automatic context sync enabled |
| Browser Chrome Automation | `zzpsah/Browser-Chrome-Automation` | target repo `.ai/PROJECT.md` | Browser automation; DevOS portable memory + automatic context sync enabled |

For registered external projects, resolve the authoritative repository first and then read that repository's `AGENTS.md`, `.ai/manifest.yaml`, `.ai/STATE-INDEX.md`, `.ai/PROJECT.md`, and `.ai/CURRENT-STATE.md`.

Add new projects only after identifying their authoritative repository.
