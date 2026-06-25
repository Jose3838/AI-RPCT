from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "forecast_dataset_governance_v1.md"


def test_forecast_dataset_governance_report_exists():
    assert REPORT.exists()


def test_forecast_dataset_blocks_ml_training():
    text = REPORT.read_text(encoding="utf-8")
    assert "ML training is not allowed" in text


def test_forecast_dataset_blocks_production_promotion():
    text = REPORT.read_text(encoding="utf-8")
    assert "Production promotion is not allowed" in text


def test_forecast_dataset_declares_feature_only():
    text = REPORT.read_text(encoding="utf-8")
    assert "feature-only" in text
