import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analytics"))

import run_pipeline


def test_load_steps_reads_pipeline_manifest():
    steps = run_pipeline.load_steps(ROOT / "config" / "pipeline.yaml")

    assert len(steps) > 0
    assert "build_feature_store" in steps


def test_script_name_adds_py_suffix():
    assert run_pipeline.script_name("build_feature_store") == "build_feature_store.py"


def test_script_name_keeps_py_suffix():
    assert run_pipeline.script_name("build_feature_store.py") == "build_feature_store.py"


def test_discover_available_steps_finds_builders():
    available = run_pipeline.discover_available_steps()

    assert "build_feature_store" in available
    assert "build_forecast_dataset" in available


def test_resolve_script_rejects_missing_step():
    with pytest.raises(FileNotFoundError):
        run_pipeline.resolve_script("missing_step_for_test")


def test_validate_manifest_steps_rejects_missing_step():
    with pytest.raises(FileNotFoundError):
        run_pipeline.validate_manifest_steps(["missing_step_for_test"])
