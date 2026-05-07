# Research: T-Shirt Size Effort Estimator

**Phase 0 output** | **Branch**: `001-tshirt-effort-estimator` | **Date**: 2026-05-07

## Language & Runtime

**Decision**: Python 3.11+

**Rationale**: Python has the strongest Anthropic SDK support and the richest ecosystem
for LLM-integrated CLI tools. The standard library covers all CLI, logging, and JSON
needs without extra dependencies. Pytest provides excellent test isolation and
parametrization.

**Alternatives considered**:
- Node.js — good Anthropic SDK but less natural for data-processing pipelines and lacks
  a stdlib argparse equivalent.
- Go — fast and single-binary but verbose for LLM-integration and mocking in tests.
- Rust — zero-overhead but engineering cost far exceeds the problem scope (YAGNI).

---

## Estimation Approach

**Decision**: LLM-based estimation via the Anthropic Claude API (claude-sonnet-4-6 or
current recommended model).

**Rationale**: Task descriptions are free-form natural language. A rule-based heuristic
would require extensive hand-crafted keyword maps and would fail for novel or ambiguous
task types. An LLM interprets intent, infers scope, and can surface explicit assumptions
when input is vague — exactly matching the spec's requirements.

The prompt is versioned as a module-level constant so changes are tracked in git and
auditable (Principle II). The prompt instructs the model to: (a) select one of the six
sizes, (b) provide a 1–3 sentence rationale referencing specific task description
elements, and (c) list any assumptions made for vague inputs.

**Alternatives considered**:
- Rule-based keyword scoring — brittle, cannot generalise to novel task descriptions.
- Local fine-tuned classifier — requires labelled training data we do not have; also
  violates YAGNI.
- Embedding similarity to reference tasks — needs a curated reference corpus; more
  complexity than the problem warrants.

---

## CLI Framework

**Decision**: Python `argparse` (standard library)

**Rationale**: Zero external dependencies. Sufficient for the subcommand structure
required (estimate, sizes). Aligns with Simplicity / YAGNI.

**Alternatives considered**:
- Click — ergonomic decorator API but adds an external dependency not justified by
  this tool's scope.
- Typer — modern type-annotated CLI framework; excellent DX but another dependency
  with no material benefit at this scale.

---

## T-Shirt Size Scale

**Decision**: Six-point scale with the following definitions:

| Size | Effort Range      | Scope Indicators                                              |
|------|-------------------|---------------------------------------------------------------|
| XS   | < half a day      | Isolated change; well-understood; no design needed            |
| S    | Half–1 day        | Small, clear-scope change; minimal testing surface            |
| M    | 2–3 days          | Moderate complexity; some design; standard test coverage      |
| L    | 1–2 weeks         | Significant work; planning required; integration concerns     |
| XL   | 2–4 weeks         | Complex feature; multiple components; possible cross-team     |
| XXL  | > 1 month         | Epic-level; MUST be decomposed before meaningful estimation   |

**Rationale**: Six levels provide enough resolution to be useful while remaining simple
enough to agree on without argument. The definitions anchor each level to effort ranges
(not calendar duration), consistent with Principle I's "stated basis" requirement.

**Alternatives considered**:
- Four sizes (S/M/L/XL) — less resolution; M would cover too wide a range.
- Eight sizes with XL+ variants — too granular; invites false precision (violates
  Principle I).
- Story-points instead of t-shirt sizes — out of scope per user description.

---

## Testing Framework

**Decision**: pytest with `unittest.mock` for LLM call isolation

**Rationale**: pytest is the de facto standard for Python. Parametrized test cases
handle the six-size matrix efficiently. `unittest.mock` is stdlib and sufficient for
patching Anthropic API calls. No third-party mocking library needed.

**Alternatives considered**:
- `unittest` only — less ergonomic; no parametrize without plugins.
- `responses` / `httpretty` — network-level mocking; unnecessary when patching the SDK
  client object directly.

---

## Structured Output & Logging

**Decision**:
- Human-readable output to stdout by default.
- `--format json` flag emits a JSON object: `{"size": "M", "rationale": "...",
  "assumptions": [...]}`.
- All debug/info logs and errors go to stderr via Python `logging` (never mixed into
  stdout).

**Rationale**: Matches the CLI Contract standard in the constitution. Keeps stdout
parseable regardless of log verbosity.

---

## Prompt Versioning

**Decision**: Estimation prompt stored as `ESTIMATION_PROMPT_V1` constant in
`src/prompts.py`. Version suffix increments when the prompt changes semantics. Changelog
entry required for any bump (Principle II).

**Rationale**: Version in the constant name makes changes visible in git blame and diff
without requiring a separate metadata file.
