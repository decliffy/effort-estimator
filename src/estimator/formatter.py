import json
from typing import Union

from estimator.models import (
    BatchEstimationResult,
    EstimationError,
    EstimationResult,
)
from estimator.sizes import SIZE_DEFINITIONS


def format_result(result: EstimationResult, fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps(
            {
                "size": result.size.value,
                "rationale": result.rationale,
                "assumptions": result.assumptions,
            },
            indent=2,
        )
    lines = [
        f"Size:       {result.size.value}",
        f"Rationale:  {result.rationale}",
    ]
    if result.assumptions:
        lines.append("Assumptions:")
        for assumption in result.assumptions:
            lines.append(f"  - {assumption}")
    else:
        lines.append("Assumptions: (none)")
    return "\n".join(lines)


def format_batch_result(batch_result: BatchEstimationResult, fmt: str = "text") -> str:
    if fmt == "json":
        items = []
        for i, r in enumerate(batch_result.results, start=1):
            if isinstance(r, EstimationResult):
                items.append(
                    {
                        "index": i,
                        "size": r.size.value,
                        "rationale": r.rationale,
                        "assumptions": r.assumptions,
                    }
                )
            else:
                items.append({"index": i, "error": r.message})
        return json.dumps(items, indent=2)

    lines = []
    for i, r in enumerate(batch_result.results, start=1):
        if isinstance(r, EstimationResult):
            lines.append(f"[{i}] Size: {r.size.value:<3} | Rationale: {r.rationale}")
        else:
            lines.append(f"[{i}] ERROR | {r.message}")
    return "\n".join(lines)


def format_sizes(fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps(
            [
                {
                    "size": sd.size.value,
                    "effort_range": sd.effort_range,
                    "description": sd.description,
                    "indicators": sd.indicators,
                }
                for sd in SIZE_DEFINITIONS
            ],
            indent=2,
        )
    col_size = max(len(sd.size.value) for sd in SIZE_DEFINITIONS)
    col_range = max(len(sd.effort_range) for sd in SIZE_DEFINITIONS)
    lines = []
    for sd in SIZE_DEFINITIONS:
        lines.append(
            f"{sd.size.value:<{col_size}}  | {sd.effort_range:<{col_range}}  | {sd.description}"
        )
    return "\n".join(lines)
