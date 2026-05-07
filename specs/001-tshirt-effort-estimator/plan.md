# Implementation Plan: T-Shirt Size Effort Estimator

**Branch**: `001-tshirt-effort-estimator` | **Date**: 2026-05-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-tshirt-effort-estimator/spec.md`

## Summary

Build a Python CLI tool (`estimate`) that accepts a free-text task description and
returns a t-shirt size estimate (XS/S/M/L/XL/XXL) plus a rationale by calling the
Anthropic Claude API. Supports single-task, batch, and stdin input modes. Output is
either human-readable text or JSON. No persistence; fully stateless.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `anthropic` SDK (LLM calls); stdlib only for CLI, logging, JSON
**Storage**: N/A — stateless; no persistence
**Testing**: pytest + `unittest.mock` (stdlib)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: CLI tool
**Performance Goals**: Single estimate returned in under 10 seconds (SC-001); batch of
10 tasks in under 60 seconds (SC-004)
**Constraints**: Stateless; no DB; no auth; `ANTHROPIC_API_KEY` env var required
**Scale/Scope**: Single-user; no concurrency requirements

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status | Notes |
|-----------|------|--------|-------|
| I — Accuracy Over Precision | Estimates MUST use ranges (t-shirt sizes), not point values; MUST include stated basis (rationale + assumptions) | ✅ PASS | T-shirt sizes are inherently ranges. Every output includes rationale and surfaces assumptions when input is vague. |
| II — Transparency & Explainability | Logic MUST be documented and auditable; prompt MUST be versioned | ✅ PASS | Prompt stored as `ESTIMATION_PROMPT_V1` constant in `src/prompts.py`; changes tracked in git. Users always see the rationale. |
| III — Test-First (NON-NEGOTIABLE) | Tests MUST be written before implementation; Red-Green-Refactor enforced | ✅ PASS | Tasks are ordered: tests first, then implementation. No implementation task may start until its test task is complete. |
| IV — Simplicity (YAGNI) | Start with simplest approach; justify any added complexity | ✅ PASS | stdlib argparse over Click/Typer; no DB; no auth; no persistence. Single source tree. |
| V — Observability | All operations MUST emit structured logs; errors MUST surface explicitly via stderr | ✅ PASS | Python `logging` to stderr; `--verbose` flag; errors never swallowed; JSON output mode for machine consumption. |

**Post-design re-check**: All gates pass. No violations. No Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/001-tshirt-effort-estimator/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── cli-contract.md  # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root)

```text
src/
├── estimator/
│   ├── __init__.py
│   ├── __main__.py       # Entry point: python -m estimator
│   ├── cli.py            # argparse setup and subcommands
│   ├── sizes.py          # TShirtSize enum + SizeDefinition constants
│   ├── models.py         # EstimationRequest, EstimationResult, EstimationError
│   ├── prompts.py        # ESTIMATION_PROMPT_V1 constant
│   ├── estimator.py      # Core estimation logic (calls LLM, parses response)
│   └── formatter.py      # Text and JSON output formatting

tests/
├── contract/
│   └── test_cli_contract.py    # Contract tests: CLI inputs/outputs/exit codes
├── integration/
│   └── test_estimation_flow.py # End-to-end flow with mocked LLM
└── unit/
    ├── test_sizes.py           # SizeDefinition completeness, enum validation
    ├── test_models.py          # Validation rules for request/result entities
    ├── test_prompts.py         # Prompt construction correctness
    ├── test_estimator.py       # LLM call, response parsing, error handling
    └── test_formatter.py       # Text and JSON output formatting

pyproject.toml            # Project metadata, dependencies, entry point
```

**Structure Decision**: Single-project layout (Option 1). The tool is a pure CLI with
no frontend or mobile surface. All source under `src/estimator/`, tests under `tests/`.

## Complexity Tracking

> No violations to justify. All constitution gates pass without exception.
