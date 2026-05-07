---
description: "Task list for T-Shirt Size Effort Estimator"
---

# Tasks: T-Shirt Size Effort Estimator

**Input**: Design documents from `specs/001-tshirt-effort-estimator/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/cli-contract.md ✅

**Tests**: Included in every phase per constitution Principle III (Test-First is NON-NEGOTIABLE).
All test tasks MUST fail (RED) before their paired implementation tasks are started.

**Organization**: Tasks are grouped by user story to enable independent implementation
and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths are included in every task description

## Path Conventions

Single-project layout per plan.md:

- Source: `src/estimator/`
- Tests: `tests/contract/`, `tests/integration/`, `tests/unit/`

---

## Phase 1: Setup

**Purpose**: Initialize project structure and tooling

- [ ] T001 Create directory tree: `src/estimator/`, `tests/contract/`, `tests/integration/`, `tests/unit/`
- [ ] T002 Create `pyproject.toml` with package metadata, `anthropic` dependency, pytest config, and `estimate` entry point pointing to `src/estimator/cli:main`
- [ ] T003 [P] Create empty `__init__.py` files in `src/estimator/`, `tests/contract/`, `tests/integration/`, `tests/unit/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core types, models, prompt constant, logging, and CLI skeleton that ALL
user stories depend on. Tests are written first (RED), then implementation (GREEN).

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

### Tests (write first — must FAIL before implementation)

- [ ] T004 [P] Write unit tests for `TShirtSize` enum (all six values present, no extras) and `SizeDefinition` completeness (all fields populated for every size) in `tests/unit/test_sizes.py`
- [ ] T005 [P] Write unit tests for `EstimationRequest` validation (empty input rejected, whitespace-only rejected, long input flagged), `EstimationResult` invariants (rationale non-empty, size is valid enum value), and `EstimationError` structure in `tests/unit/test_models.py`
- [ ] T006 [P] Write unit tests for `ESTIMATION_PROMPT_V1` in `tests/unit/test_prompts.py`: verify prompt contains size list, instructs model to return rationale, and includes assumptions instruction

### Implementation (after tests are RED)

- [ ] T007 Implement `TShirtSize` enum (XS/S/M/L/XL/XXL) in `src/estimator/sizes.py` — GREEN for T004
- [ ] T008 [P] Implement `SizeDefinition` dataclass and `SIZE_DEFINITIONS` constant (all six sizes with effort_range, description, indicators) in `src/estimator/sizes.py` — GREEN for T004
- [ ] T009 Implement `EstimationRequest`, `EstimationResult`, `EstimationError` dataclasses with validation in `src/estimator/models.py` — GREEN for T005
- [ ] T010 Implement `ESTIMATION_PROMPT_V1` constant in `src/estimator/prompts.py` — GREEN for T006
- [ ] T011 Configure stderr logging with `--verbose` flag support in `src/estimator/__init__.py`
- [ ] T012 Add `ANTHROPIC_API_KEY` environment variable check with clear error to stderr and exit code 1 in `src/estimator/cli.py`
- [ ] T013 Create argparse CLI skeleton with subcommand structure (`estimate`, `sizes`) and `--format` / `--verbose` / `--batch` flags in `src/estimator/cli.py` and `src/estimator/__main__.py`

**Checkpoint**: Foundation ready — all foundational tests pass, API key check works, CLI skeleton runs

---

## Phase 3: User Story 1 — Get Effort Estimate for a Task (Priority: P1) 🎯 MVP

**Goal**: User submits a task description and receives a t-shirt size with rationale.

**Independent Test**: Run `estimate "Add pagination to the user list endpoint"` and
verify a valid size (XS–XXL) and non-empty rationale are returned referencing the input.

### Tests for User Story 1 ⚠️ Write first — must FAIL before implementation

- [ ] T014 [P] [US1] Write contract test for `estimate <description>`: valid input returns size + rationale; empty input exits with code 1 and error on stderr; missing API key exits with code 1 in `tests/contract/test_cli_contract.py`
- [ ] T015 [P] [US1] Write unit tests for `estimator.py`: LLM call invoked with correct prompt, response parsed to `EstimationResult`, API error raises `EstimationError`, malformed LLM response raises `EstimationError` in `tests/unit/test_estimator.py`
- [ ] T016 [P] [US1] Write unit tests for `formatter.py`: text output format matches spec, JSON output is valid and contains `size`/`rationale`/`assumptions` keys in `tests/unit/test_formatter.py`
- [ ] T017 [P] [US1] Write integration test for single estimate flow (mock LLM, verify end-to-end path from CLI args through formatter to stdout) in `tests/integration/test_estimation_flow.py`

### Implementation for User Story 1

- [ ] T018 [US1] Implement Anthropic API call using `ESTIMATION_PROMPT_V1` and parse LLM response into `EstimationResult` in `src/estimator/estimator.py` — GREEN for T015
- [ ] T019 [US1] Add input validation (empty/whitespace → `EstimationError`; >4000 chars → truncate and note in rationale) to `src/estimator/estimator.py`
- [ ] T020 [US1] Add structured logging for each estimation operation (input length, size returned, latency) in `src/estimator/estimator.py`
- [ ] T021 [US1] Implement text and JSON output formatting for `EstimationResult` in `src/estimator/formatter.py` — GREEN for T016
- [ ] T022 [US1] Wire `estimate <description>` subcommand and stdin fallback into `src/estimator/cli.py`; emit output to stdout, errors to stderr — GREEN for T014, T017

**Checkpoint**: User Story 1 is fully functional and independently testable. Run
`estimate "Write a unit test for the login service"` and validate output.

---

## Phase 4: User Story 2 — Understand What Each Size Means (Priority: P2)

**Goal**: User can view definitions for all six t-shirt sizes.

**Independent Test**: Run `estimate sizes` and verify all six sizes (XS–XXL) appear
with effort_range, description, and indicators. Run `estimate sizes --format json` and
verify valid JSON array with correct keys.

### Tests for User Story 2 ⚠️ Write first — must FAIL before implementation

- [ ] T023 [P] [US2] Write contract test for `estimate sizes`: all six sizes present in text output; `--format json` returns valid JSON array with required keys per cli-contract.md in `tests/contract/test_cli_contract.py`

### Implementation for User Story 2

- [ ] T024 [US2] Implement `estimate sizes` subcommand that reads `SIZE_DEFINITIONS` and formats output (text table + JSON array) in `src/estimator/cli.py` and `src/estimator/formatter.py` — GREEN for T023

**Checkpoint**: User Story 2 is fully functional and independently testable. Run
`estimate sizes` and `estimate sizes --format json` to validate.

---

## Phase 5: User Story 3 — Batch Estimate Multiple Tasks (Priority: P3)

**Goal**: User provides a file of task descriptions and receives an estimate per line.

**Independent Test**: Create a 3-line tasks.txt (one empty line), run
`estimate --batch tasks.txt`, and verify 2 valid estimates plus 1 per-item error are
returned in input order with exit code 0.

### Tests for User Story 3 ⚠️ Write first — must FAIL before implementation

- [ ] T025 [P] [US3] Write contract test for `estimate --batch <file>`: valid file returns ordered estimates; one invalid line returns per-item error without blocking others; missing file exits with code 1 in `tests/contract/test_cli_contract.py`
- [ ] T026 [P] [US3] Write unit tests for `BatchEstimationRequest` (empty list rejected) and `BatchEstimationResult` (same length as input, order preserved) in `tests/unit/test_models.py`
- [ ] T027 [P] [US3] Write integration test for batch flow: mock LLM returns fixture responses, verify output order and per-item error handling in `tests/integration/test_estimation_flow.py`

### Implementation for User Story 3

- [ ] T028 [US3] Implement `BatchEstimationRequest` and `BatchEstimationResult` in `src/estimator/models.py` — GREEN for T026
- [ ] T029 [US3] Implement batch estimation logic (iterate tasks, collect results + errors, preserve order) in `src/estimator/estimator.py` — GREEN for T027
- [ ] T030 [US3] Implement batch text and JSON output formatting in `src/estimator/formatter.py`
- [ ] T031 [US3] Wire `--batch <file>` flag into `src/estimator/cli.py` (read file, validate, dispatch to batch estimator, write output) — GREEN for T025

**Checkpoint**: All three user stories independently functional. Run the batch quickstart
scenario from `quickstart.md` to validate.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect all user stories

- [ ] T032 [P] Add `--help` text with usage examples to all subcommands in `src/estimator/cli.py`
- [ ] T033 Code cleanup: refactor any duplication across `estimator.py`, `formatter.py`, `cli.py`
- [ ] T034 [P] Add `README.md` at repository root with installation steps, usage examples, and environment variable reference
- [ ] T035 Run full quickstart.md validation end-to-end (setup → single estimate → sizes → batch → stdin pipe)
- [ ] T036 [P] Security hardening: ensure API key is never logged or included in stdout output

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 — MVP; no other story dependencies
- **User Story 2 (Phase 4)**: Depends on Phase 2 — no dependency on US1
- **User Story 3 (Phase 5)**: Depends on Phase 2 and US1 (batch uses single-estimate logic)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — no story dependencies
- **US2 (P2)**: Can start after Phase 2 — no story dependencies; parallelizable with US1
- **US3 (P3)**: Depends on US1 (batch reuses `estimator.py` functions from US1)

### Within Each User Story

- Tests MUST be written and FAIL before implementation begins
- Models before services before CLI wiring
- Story complete and checkpoint validated before moving to next priority

### Parallel Opportunities

- T004, T005, T006 (foundational tests) — all parallel
- T007, T008, T009, T010 (foundational impl, different files) — T007+T008 parallel after T004; T009 after T005; T010 after T006
- T014, T015, T016, T017 (US1 tests) — all parallel
- T023 (US2 test) can run in parallel with US1 implementation
- T025, T026, T027 (US3 tests) — all parallel

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all US1 tests together (all must FAIL before implementation):
Task: "T014 — contract test for estimate <description>"
Task: "T015 — unit test for estimator.py"
Task: "T016 — unit test for formatter.py"
Task: "T017 — integration test for single estimate flow"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational — CRITICAL, blocks everything
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: `estimate "Add pagination to user list"` returns valid output
5. Demo / deploy MVP

### Incremental Delivery

1. Setup + Foundational → foundation ready
2. US1 → single estimate MVP ✅ demo-ready
3. US2 → sizes help ✅ demo-ready
4. US3 → batch mode ✅ demo-ready
5. Polish → production-ready

### Parallel Team Strategy

With two developers after Phase 2 completes:
- Developer A: User Story 1 (Phase 3)
- Developer B: User Story 2 (Phase 4)
- Both merge → Developer A/B: User Story 3 (Phase 5)

---

## Notes

- `[P]` tasks touch different files and have no incomplete dependencies — safe to parallelize
- `[US#]` label maps task to a specific user story for traceability
- Every story phase can be independently completed and tested before moving on
- Tests MUST be RED before implementation; never start T018+ before T014–T017 are failing
- Commit after each checkpoint (constitution Development Workflow requirement)
- `ANTHROPIC_API_KEY` must be set in the environment for integration tests to run against the live API; unit and contract tests use mocks and do not require it
