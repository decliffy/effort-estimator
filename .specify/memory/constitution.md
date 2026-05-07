<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 1.0.0 (no change — validation run only)

Modified principles: None

Added sections: None

Removed sections: None

Templates requiring updates:
  ✅ .specify/templates/plan-template.md — Constitution Check placeholder
     `[Gates determined based on constitution file]` is per-feature and filled
     by /speckit-plan; no structural update required.
  ✅ .specify/templates/spec-template.md — No constitution-specific references;
     structure is compatible with all five principles.
  ✅ .specify/templates/tasks-template.md — Test-first ordering aligns with
     Principle III; no update required.
  ✅ .specify/templates/commands/ — No command files found; nothing to update.
  ✅ README.md — Not present; nothing to update.

Follow-up TODOs:
  - TODO(TECH_STACK): Primary language, runtime version, and testing framework
    must be confirmed once the technology stack decision is made and encoded in
    Technical Standards.
-->

# Effort Estimator Constitution

## Core Principles

### I. Accuracy Over Precision

Estimates MUST represent uncertainty with ranges or confidence intervals rather than
false-precision point values. Every estimate output MUST include a stated basis
(inputs used, assumptions made) so consumers can recalibrate when conditions change.
Overconfident single-point estimates with no uncertainty disclosure are treated as
defects, not features.

### II. Transparency & Explainability

Every estimate MUST be fully traceable to its inputs and the model or heuristic that
produced it. Black-box outputs are not acceptable. Estimation logic MUST be documented
and auditable; changes to estimation algorithms MUST be versioned and recorded in a
changelog. Users MUST be able to understand *why* an estimate was produced, not just
*what* was produced.

### III. Test-First (NON-NEGOTIABLE)

TDD is mandatory across all features. Tests MUST be written and reviewed before
implementation begins. The Red-Green-Refactor cycle is strictly enforced: tests MUST
fail before implementation, pass after, and the code MUST be refactored before the
task is considered done. No feature is complete without passing tests that cover the
primary acceptance scenarios defined in its spec.

### IV. Simplicity (YAGNI)

Implementation MUST start with the simplest approach that satisfies current requirements.
Abstractions are introduced only when a concrete duplication or constraint forces them —
not in anticipation of hypothetical future needs. Any added complexity MUST be explicitly
justified and recorded in the plan's Complexity Tracking table. Three similar lines of
code are preferable to a premature abstraction.

### V. Observability

All estimation operations MUST emit structured logs sufficient to reproduce any given
estimate from its inputs alone. Errors and edge cases (e.g., out-of-range inputs,
unrecognized task types, missing required fields) MUST be surfaced clearly and
explicitly — via stderr or a structured error payload — never silently defaulted or
swallowed. Debuggability is a first-class requirement.

## Technical Standards

Technology choices and constraints that apply across all features of this project.

- **Language/Runtime**: TODO(TECH_STACK): Confirm primary language and runtime version
  once the technology stack is decided. Record the decision here.
- **Testing Framework**: MUST use a framework supporting isolated unit tests and
  integration tests. Contract tests MUST be included for any public API surface.
- **CLI Contract**: If a CLI is exposed, it MUST follow the text-in/text-out convention:
  arguments or stdin → stdout; errors → stderr. MUST support both human-readable and
  JSON output formats via a flag (e.g., `--format json`).
- **No External State Without Justification**: Features MUST NOT introduce databases,
  external services, or persistent state unless the feature specification explicitly
  requires it and the plan's Complexity Tracking table justifies why a simpler approach
  is insufficient.

## Development Workflow

Standards governing how features move from idea to production.

- All feature work MUST begin with a dedicated feature branch (`/speckit-git-feature`).
- A reviewed spec MUST exist before planning (`/speckit-plan`) begins.
- All tasks in `tasks.md` MUST map to a user story from `spec.md`.
- Each user story MUST be independently testable and demonstrable as an MVP increment.
- Commits MUST be atomic: one logical change per commit with a descriptive message.
- PRs MUST pass all tests and satisfy every gate in the plan's Constitution Check
  section before merging. Non-compliance MUST be resolved or formally exempted with
  written justification.

## Governance

This constitution supersedes all other project practices. Any practice not addressed
here defaults to the principle of Simplicity (Principle IV).

**Amendment procedure**: Amendments MUST be proposed as a diff to this file with a
clear rationale. The version bump type (MAJOR/MINOR/PATCH) MUST be declared and agreed
upon before the amendment is merged. All dependent templates listed in the Sync Impact
Report MUST be reviewed and updated within the same change.

**Versioning policy**:
- MAJOR — backward-incompatible governance change; principle removal or incompatible
  redefinition.
- MINOR — new principle or section added; materially expanded guidance.
- PATCH — clarifications, wording improvements, typo fixes; no semantic change.

**Compliance review**: Every plan's Constitution Check section MUST explicitly verify
compliance with each applicable principle before implementation begins. Gaps MUST be
flagged and either resolved or formally exempted with justification recorded in the
plan's Complexity Tracking table.

**Version**: 1.0.0 | **Ratified**: 2026-05-06 | **Last Amended**: 2026-05-06
