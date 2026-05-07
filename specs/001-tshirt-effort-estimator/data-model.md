# Data Model: T-Shirt Size Effort Estimator

**Phase 1 output** | **Branch**: `001-tshirt-effort-estimator` | **Date**: 2026-05-07

## Entities

### TShirtSize (Enum)

The fixed set of valid estimate values.

| Value | Label |
|-------|-------|
| XS    | Extra Small |
| S     | Small |
| M     | Medium |
| L     | Large |
| XL    | Extra Large |
| XXL   | Extra Extra Large |

**Validation**: Any output not in this set is a defect. The LLM response parser MUST
reject and surface an error if the model returns an unrecognised value.

---

### SizeDefinition

A human-readable description of what each `TShirtSize` value means.

| Field          | Type         | Constraints                          |
|----------------|--------------|--------------------------------------|
| `size`         | TShirtSize   | Required; unique key                 |
| `effort_range` | str          | Required; e.g. "2–3 days"            |
| `description`  | str          | Required; 1 sentence summary         |
| `indicators`   | list[str]    | Required; ≥ 1 scope signal           |

**Notes**: `SizeDefinition` values are static constants defined in `src/sizes.py`.
They are not persisted and never change at runtime.

---

### EstimationRequest

Represents a single estimation input.

| Field         | Type      | Constraints                                    |
|---------------|-----------|------------------------------------------------|
| `description` | str       | Required; non-empty after stripping whitespace |

**Validation rules**:
- `description` MUST NOT be empty or whitespace-only → return error, no estimate.
- `description` longer than 4000 characters MAY be truncated; truncation MUST be
  disclosed in the rationale (FR-001, edge case in spec).

---

### EstimationResult

Represents the output for a single estimation.

| Field         | Type           | Constraints                                      |
|---------------|----------------|--------------------------------------------------|
| `request`     | EstimationRequest | Required; the originating request             |
| `size`        | TShirtSize     | Required; one of the six valid sizes             |
| `rationale`   | str            | Required; 1–3 sentences; references input text   |
| `assumptions` | list[str]      | Optional; present when vague input detected      |

**Invariants**:
- `rationale` MUST reference at least one element from `request.description`.
- If `assumptions` is non-empty, at least one assumption MUST appear in `rationale`.
- `size` MUST be a valid `TShirtSize` enum value.

---

### BatchEstimationRequest

Represents a multi-task estimation input.

| Field    | Type                    | Constraints                  |
|----------|-------------------------|------------------------------|
| `tasks`  | list[EstimationRequest] | Required; ≥ 1 item           |

**Validation rules**:
- Empty list → error: "No tasks provided".
- Individual invalid tasks are surfaced per-item; other tasks still proceed.

---

### BatchEstimationResult

Represents the output for a batch estimation.

| Field     | Type                    | Constraints                                    |
|-----------|-------------------------|------------------------------------------------|
| `results` | list[EstimationResult \| EstimationError] | Ordered; same length as input |

---

### EstimationError

Represents a failed estimation for one task (used in batch mode).

| Field     | Type   | Constraints                     |
|-----------|--------|---------------------------------|
| `request` | EstimationRequest | The originating request |
| `message` | str    | Required; human-readable reason |

---

## State Transitions

The tool is stateless. Each invocation is independent. No state persists between calls.

```
Input received
    │
    ▼
Validate (non-empty, length check)
    │ invalid → EstimationError (to stderr)
    │ valid
    ▼
Build prompt (EstimationRequest → prompt string)
    │
    ▼
Call LLM API
    │ API error → EstimationError (to stderr)
    │ success
    ▼
Parse LLM response → EstimationResult
    │ parse error → EstimationError (to stderr)
    │ success
    ▼
Format output (human-readable or JSON)
    │
    ▼
Write to stdout
```
