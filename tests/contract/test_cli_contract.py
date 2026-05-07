import json
import subprocess
import sys
import os
import pytest


def run_estimate(*args, input_text=None, env=None):
    cmd = [sys.executable, "-m", "estimator"] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        input=input_text,
        env=env,
        cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    )
    return result


def env_with_key(key="test_api_key_placeholder"):
    e = os.environ.copy()
    e["ANTHROPIC_API_KEY"] = key
    return e


def env_without_key():
    e = os.environ.copy()
    e.pop("ANTHROPIC_API_KEY", None)
    return e


class TestEstimateCommand:
    def test_missing_api_key_exits_with_code_1(self):
        result = run_estimate("estimate", "Some task", env=env_without_key())
        assert result.returncode == 1
        assert "ANTHROPIC_API_KEY" in result.stderr

    def test_empty_description_exits_with_code_1(self):
        result = run_estimate("estimate", "", env=env_with_key())
        assert result.returncode == 1
        assert "empty" in result.stderr.lower() or "Error" in result.stderr

    def test_sizes_subcommand_shows_all_six_sizes(self):
        result = run_estimate("sizes")
        assert result.returncode == 0
        for size in ["XS", "S", "M", "L", "XL", "XXL"]:
            assert size in result.stdout

    def test_sizes_json_output_is_valid(self):
        result = run_estimate("sizes", "--format", "json")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert len(data) == 6
        for item in data:
            assert "size" in item
            assert "effort_range" in item
            assert "description" in item
            assert "indicators" in item


class TestBatchCommand:
    def test_missing_batch_file_exits_with_code_1(self, tmp_path):
        result = run_estimate(
            "estimate", "--batch", str(tmp_path / "nonexistent.txt"),
            env=env_with_key(),
        )
        assert result.returncode == 1

    def test_sizes_text_output_contains_effort_range(self):
        result = run_estimate("sizes")
        assert result.returncode == 0
        assert "day" in result.stdout.lower() or "week" in result.stdout.lower()
