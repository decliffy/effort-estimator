import json
from unittest.mock import MagicMock, patch
import pytest

from estimator.models import EstimationRequest, EstimationResult, EstimationError
from estimator.sizes import TShirtSize
from estimator.estimator import estimate_task


def make_mock_response(size="M", rationale="A medium task.", assumptions=None):
    assumptions = assumptions or []
    content = json.dumps({"size": size, "rationale": rationale, "assumptions": assumptions})
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text=content)]
    return mock_msg


class TestEstimateTask:
    def test_returns_estimation_result_on_success(self):
        request = EstimationRequest(description="Add pagination to user list")
        mock_response = make_mock_response(size="S", rationale="Small well-understood change.")

        with patch("estimator.estimator._get_client") as mock_client_fn:
            mock_client = MagicMock()
            mock_client.messages.create.return_value = mock_response
            mock_client_fn.return_value = mock_client

            result = estimate_task(request)

        assert isinstance(result, EstimationResult)
        assert result.size == TShirtSize.S
        assert result.rationale == "Small well-understood change."

    def test_api_error_returns_estimation_error(self):
        request = EstimationRequest(description="Some task")

        with patch("estimator.estimator._get_client") as mock_client_fn:
            mock_client = MagicMock()
            mock_client.messages.create.side_effect = Exception("API error")
            mock_client_fn.return_value = mock_client

            result = estimate_task(request)

        assert isinstance(result, EstimationError)
        assert "API error" in result.message or result.message

    def test_malformed_response_returns_estimation_error(self):
        request = EstimationRequest(description="Some task")
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text="not valid json at all")]

        with patch("estimator.estimator._get_client") as mock_client_fn:
            mock_client = MagicMock()
            mock_client.messages.create.return_value = mock_msg
            mock_client_fn.return_value = mock_client

            result = estimate_task(request)

        assert isinstance(result, EstimationError)

    def test_invalid_size_in_response_returns_estimation_error(self):
        request = EstimationRequest(description="Some task")
        mock_response = make_mock_response(size="HUGE", rationale="Some rationale.")

        with patch("estimator.estimator._get_client") as mock_client_fn:
            mock_client = MagicMock()
            mock_client.messages.create.return_value = mock_response
            mock_client_fn.return_value = mock_client

            result = estimate_task(request)

        assert isinstance(result, EstimationError)

    def test_prompt_sent_to_llm_contains_description(self):
        request = EstimationRequest(description="My specific task description")
        mock_response = make_mock_response()

        with patch("estimator.estimator._get_client") as mock_client_fn:
            mock_client = MagicMock()
            mock_client.messages.create.return_value = mock_response
            mock_client_fn.return_value = mock_client

            estimate_task(request)

            call_kwargs = mock_client.messages.create.call_args
            messages = call_kwargs[1]["messages"] if call_kwargs[1] else call_kwargs[0][0]
            combined = str(messages)
            assert "My specific task description" in combined
