# CLI Contract: T-Shirt Size Effort Estimator

**Phase 1 output** | **Branch**: `001-tshirt-effort-estimator` | **Date**: 2026-05-07

## Overview

The tool is invoked as `estimate` (or `python -m estimator`). All output goes to stdout;
all errors and logs go to stderr. Exit code 0 = success; non-zero = failure.

---

## Commands

### `estimate <description>`

Estimate the effort for a single task.

**Usage**:
```
estimate [--format <fmt>] [--verbose] <description>
```

**Arguments**:

| Argument       | Type   | Required | Description                                   |
|----------------|--------|----------|-----------------------------------------------|
| `description`  | str    | Yes      | Free-text task description (quote if it contains spaces) |

**Flags**:

| Flag              | Default  | Description                          |
|-------------------|----------|--------------------------------------|
| `--format <fmt>`  | `text`   | Output format: `text` or `json`      |
| `--verbose`       | off      | Emit debug logs to stderr            |

**Text output** (stdout):
```
Size:       M
Rationale:  This task requires designing a new data schema and updating three
            existing service layers. The integration surface is moderate.
Assumptions: (none)
```

**JSON output** (stdout, `--format json`):
```json
{
  "size": "M",
  "rationale": "This task requires designing a new data schema...",
  "assumptions": []
}
```

**Error output** (stderr):
```
Error: Task description must not be empty.
```

**Exit codes**:
- `0` — estimate produced successfully
- `1` — invalid input (empty description, etc.)
- `2` — API error (LLM call failed)
- `3` — parse error (unexpected LLM response format)

---

### `estimate sizes`

Display the definition of all six t-shirt sizes.

**Usage**:
```
estimate sizes [--format <fmt>]
```

**Text output** (stdout):
```
XS  | < half a day   | Isolated change; well-understood; no design needed
S   | Half–1 day     | Small, clear-scope change; minimal testing surface
M   | 2–3 days       | Moderate complexity; some design; standard test coverage
L   | 1–2 weeks      | Significant work; planning required; integration concerns
XL  | 2–4 weeks      | Complex feature; multiple components; possible cross-team
XXL | > 1 month      | Epic-level; MUST be decomposed before meaningful estimation
```

**JSON output** (stdout, `--format json`):
```json
[
  {
    "size": "XS",
    "effort_range": "< half a day",
    "description": "Isolated change; well-understood; no design needed",
    "indicators": ["single file change", "no new abstractions", "< 50 lines"]
  },
  ...
]
```

---

### `estimate --batch <file>`

Estimate effort for multiple tasks from a file (one task per line).

**Usage**:
```
estimate --batch <file> [--format <fmt>] [--verbose]
```

**Arguments**:

| Argument  | Type      | Required | Description                             |
|-----------|-----------|----------|-----------------------------------------|
| `--batch` | file path | Yes      | Path to plain-text file; one task per line |

**Text output** (stdout):
```
[1] Size: S   | Rationale: Simple config change with no logic impact.
[2] Size: L   | Rationale: Requires cross-service coordination and new API surface.
[3] ERROR     | Task description must not be empty. (line 3)
```

**JSON output** (stdout, `--format json`):
```json
[
  {"index": 1, "size": "S", "rationale": "...", "assumptions": []},
  {"index": 2, "size": "L", "rationale": "...", "assumptions": []},
  {"index": 3, "error": "Task description must not be empty."}
]
```

**Exit codes**:
- `0` — all tasks estimated (even if some returned per-item errors)
- `1` — file not found or unreadable
- `2` — all tasks failed (API error)

---

## Environment Variables

| Variable              | Required | Description                                      |
|-----------------------|----------|--------------------------------------------------|
| `ANTHROPIC_API_KEY`   | Yes      | API key for the Anthropic Claude API             |

If `ANTHROPIC_API_KEY` is not set, the tool exits immediately with:
```
Error: ANTHROPIC_API_KEY environment variable is not set. (stderr)
```
Exit code: `1`

---

## Stdin Support

`estimate` also accepts the task description from stdin when no `<description>` argument
is provided:

```bash
echo "Refactor the payment service to use the new SDK" | estimate --format json
```

This enables pipeline composition without shell quoting concerns.
