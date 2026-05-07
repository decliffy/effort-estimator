import json
import pytest

from estimator.formatter import format_result, format_sizes
from estimator.models import EstimationRequest, EstimationResult
from estimator.sizes import TShirtSize


def make_result(size=TShirtSize.M, rationale="A medium task.", assumptions=None):
    req = EstimationRequest(description="Some task")
    return EstimationResult(request=req, size=size, rationale=rationale, assumptions=assumptions or [])


class TestFormatResult:
    def test_text_output_contains_size(self):
        result = make_result(size=TShirtSize.L)
        output = format_result(result, fmt="text")
        assert "L" in output

    def test_text_output_contains_rationale(self):
        result = make_result(rationale="This task is large.")
        output = format_result(result, fmt="text")
        assert "This task is large." in output

    def test_json_output_is_valid(self):
        result = make_result()
        output = format_result(result, fmt="json")
        data = json.loads(output)
        assert data["size"] == "M"
        assert "rationale" in data
        assert "assumptions" in data

    def test_json_output_includes_assumptions(self):
        result = make_result(assumptions=["Assumed greenfield project"])
        output = format_result(result, fmt="json")
        data = json.loads(output)
        assert "Assumed greenfield project" in data["assumptions"]

    def test_text_shows_assumptions_when_present(self):
        result = make_result(assumptions=["Assumed no legacy constraints"])
        output = format_result(result, fmt="text")
        assert "Assumed no legacy constraints" in output


class TestFormatSizes:
    def test_text_contains_all_sizes(self):
        output = format_sizes(fmt="text")
        for size in ["XS", "S", "M", "L", "XL", "XXL"]:
            assert size in output

    def test_json_is_list_of_six(self):
        output = format_sizes(fmt="json")
        data = json.loads(output)
        assert len(data) == 6

    def test_json_has_required_keys(self):
        output = format_sizes(fmt="json")
        data = json.loads(output)
        for item in data:
            assert "size" in item
            assert "effort_range" in item
            assert "description" in item
            assert "indicators" in item
