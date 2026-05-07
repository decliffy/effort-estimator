import pytest
from estimator.models import EstimationRequest, EstimationResult, EstimationError
from estimator.sizes import TShirtSize


class TestEstimationRequest:
    def test_valid_description_accepted(self):
        req = EstimationRequest(description="Add pagination to the user list endpoint")
        assert req.description == "Add pagination to the user list endpoint"

    def test_empty_description_raises(self):
        with pytest.raises(ValueError, match="empty"):
            EstimationRequest(description="")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="empty"):
            EstimationRequest(description="   ")

    def test_long_description_accepted_with_flag(self):
        long_desc = "x" * 4001
        req = EstimationRequest(description=long_desc)
        assert req.truncated is True

    def test_description_at_limit_not_truncated(self):
        desc = "x" * 4000
        req = EstimationRequest(description=desc)
        assert req.truncated is False


class TestEstimationResult:
    def test_valid_result(self):
        req = EstimationRequest(description="Some task")
        result = EstimationResult(
            request=req,
            size=TShirtSize.M,
            rationale="This is a medium task.",
            assumptions=[],
        )
        assert result.size == TShirtSize.M
        assert result.rationale == "This is a medium task."

    def test_empty_rationale_raises(self):
        req = EstimationRequest(description="Some task")
        with pytest.raises(ValueError, match="rationale"):
            EstimationResult(
                request=req,
                size=TShirtSize.M,
                rationale="",
                assumptions=[],
            )

    def test_invalid_size_raises(self):
        req = EstimationRequest(description="Some task")
        with pytest.raises((ValueError, TypeError)):
            EstimationResult(
                request=req,
                size="INVALID",
                rationale="Some rationale",
                assumptions=[],
            )


class TestEstimationError:
    def test_valid_error(self):
        req = EstimationRequest(description="Some task")
        err = EstimationError(request=req, message="API call failed")
        assert err.message == "API call failed"
        assert err.request is req

    def test_empty_message_raises(self):
        req = EstimationRequest(description="Some task")
        with pytest.raises(ValueError, match="message"):
            EstimationError(request=req, message="")
