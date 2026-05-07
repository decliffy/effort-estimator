import json
import os
import time
from typing import Union

import anthropic

from estimator import logger
from estimator.models import (
    BatchEstimationRequest,
    BatchEstimationResult,
    EstimationError,
    EstimationRequest,
    EstimationResult,
)
from estimator.prompts import ESTIMATION_PROMPT_V1
from estimator.sizes import TShirtSize


def _get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


def estimate_task(
    request: EstimationRequest,
) -> Union[EstimationResult, EstimationError]:
    description = request.description
    if request.truncated:
        description += "\n\n[Note: input was truncated to 4000 characters due to length]"

    logger.debug("Estimating task (length=%d, truncated=%s)", len(request.description), request.truncated)
    start = time.monotonic()

    try:
        client = _get_client()
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            messages=[
                {
                    "role": "user",
                    "content": f"{ESTIMATION_PROMPT_V1}\n\nTask description:\n{description}",
                }
            ],
        )
    except Exception as exc:
        logger.error("API call failed: %s", exc)
        return EstimationError(request=request, message=str(exc))

    elapsed = time.monotonic() - start
    raw = message.content[0].text.strip()
    logger.debug("LLM response received in %.2fs", elapsed)

    # Strip markdown code fences if the model wrapped its response in them
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]  # drop the opening ```json line
        raw = raw.rsplit("```", 1)[0]  # drop the closing ```
        raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM response as JSON: %s", raw[:200])
        return EstimationError(
            request=request,
            message=f"Unexpected response format from LLM: {raw[:100]}",
        )

    try:
        size = TShirtSize(data["size"])
    except (KeyError, ValueError) as exc:
        return EstimationError(
            request=request,
            message=f"Invalid size in LLM response: {data.get('size')!r}",
        )

    rationale = data.get("rationale", "").strip()
    if not rationale:
        return EstimationError(request=request, message="LLM returned an empty rationale.")

    assumptions = [str(a) for a in data.get("assumptions", []) if a]

    logger.info("Estimated '%s...' → %s in %.2fs", request.description[:40], size.value, elapsed)
    return EstimationResult(
        request=request,
        size=size,
        rationale=rationale,
        assumptions=assumptions,
    )


def estimate_batch(
    batch_request: BatchEstimationRequest,
    raw_lines: list[str] | None = None,
) -> BatchEstimationResult:
    results: list[Union[EstimationResult, EstimationError]] = []
    for task in batch_request.tasks:
        results.append(estimate_task(task))
    return BatchEstimationResult(results=results)
