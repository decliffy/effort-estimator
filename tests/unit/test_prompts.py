from estimator.prompts import ESTIMATION_PROMPT_V1
from estimator.sizes import TShirtSize


def test_prompt_contains_all_sizes():
    for size in TShirtSize:
        assert size.value in ESTIMATION_PROMPT_V1, (
            f"Size '{size.value}' not found in ESTIMATION_PROMPT_V1"
        )


def test_prompt_instructs_rationale():
    assert "rationale" in ESTIMATION_PROMPT_V1.lower()


def test_prompt_instructs_assumptions():
    assert "assumption" in ESTIMATION_PROMPT_V1.lower()


def test_prompt_is_nonempty_string():
    assert isinstance(ESTIMATION_PROMPT_V1, str)
    assert len(ESTIMATION_PROMPT_V1) > 100


def test_prompt_requests_structured_output():
    lower = ESTIMATION_PROMPT_V1.lower()
    assert "json" in lower or "size" in lower
