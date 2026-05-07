import json
import subprocess
import sys
import os
from unittest.mock import MagicMock, patch

import pytest

from estimator.estimator import estimate_task
from estimator.formatter import format_result
from estimator.models import EstimationRequest, EstimationResult
from estimator.sizes import TShirtSize


def make_mock_response(size="M", rationale="Moderate task.", assumptions=None):
    assumptions = assumptions or []
    content = json.dumps({"size": size, "rationale": rationale, "assumptions": assumptions})
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text=content)]
    return mock_msg


class TestSingleEstimateFlow:
    def test_end_to_end_single_estimate(self):
        request = EstimationRequest(description="Add rate limiting to the public API")
        mock_response = make_mock_response(
            size="L",
            rationale="Rate limiting requires middleware changes across the public API surface.",
        )

        with patch("estimator.estimator._get_client") as mock_client_fn:
            mock_client = MagicMock()
            mock_client.messages.create.return_value = mock_response
            mock_client_fn.return_value = mock_client

            result = estimate_task(request)

        assert isinstance(result, EstimationResult)
        assert result.size == TShirtSize.L

        text_output = format_result(result, fmt="text")
        assert "L" in text_output
        assert "Rate limiting" in text_output

        json_output = format_result(result, fmt="json")
        data = json.loads(json_output)
        assert data["size"] == "L"

    def test_truncated_input_disclosed_in_result(self):
        long_desc = "Do something important. " * 200
        request = EstimationRequest(description=long_desc)
        assert request.truncated is True

        mock_response = make_mock_response(
            size="XL",
            rationale="The description was long.",
            assumptions=["Input was truncated due to length"],
        )

        with patch("estimator.estimator._get_client") as mock_client_fn:
            mock_client = MagicMock()
            mock_client.messages.create.return_value = mock_response
            mock_client_fn.return_value = mock_client

            result = estimate_task(request)

        assert isinstance(result, EstimationResult)
        output = format_result(result, fmt="text")
        assert "XL" in output


class TestBatchEstimateFlow:
    def test_batch_end_to_end(self):
        from estimator.estimator import estimate_batch
        from estimator.formatter import format_batch_result
        from estimator.models import BatchEstimationRequest

        descriptions = [
            "Fix a typo in the docs",
            "Rewrite the authentication system",
        ]
        requests = [EstimationRequest(description=d) for d in descriptions]
        batch_req = BatchEstimationRequest(tasks=requests)

        responses = [
            make_mock_response(size="XS", rationale="Trivial doc fix."),
            make_mock_response(size="XL", rationale="Auth rewrite is complex."),
        ]

        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            resp = responses[call_count]
            call_count += 1
            return resp

        with patch("estimator.estimator._get_client") as mock_client_fn:
            mock_client = MagicMock()
            mock_client.messages.create.side_effect = side_effect
            mock_client_fn.return_value = mock_client

            batch_result = estimate_batch(batch_req)

        assert len(batch_result.results) == 2
        output = format_batch_result(batch_result, fmt="text")
        assert "XS" in output
        assert "XL" in output
