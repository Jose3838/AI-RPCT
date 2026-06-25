from pathlib import Path

import pandas as pd


def test_readiness_dashboard_pilot_state():
    path = Path("data/ai_rpct_readiness_dashboard_v1.csv")
    assert path.exists()

    df = pd.read_csv(path)
    row = df.iloc[0]

    assert row["platform_stage"] == "pilot"
    assert str(row["customer_demo_allowed"]).lower() == "true"
    assert str(row["paid_production_allowed"]).lower() == "false"
    assert str(row["ml_retraining_allowed"]).lower() == "false"


def test_training_dataset_v3_blocks_without_true_labels():
    path = Path("data/training_dataset_v3_readiness.csv")
    assert path.exists()

    df = pd.read_csv(path)
    row = df.iloc[0]

    assert row["status"] == "not_ready"
    assert int(row["trainable_label_rows"]) == 0
    assert int(row["training_rows"]) == 0


def test_auto_retraining_waits_for_labels():
    path = Path("data/auto_retraining_manager_v1.csv")
    assert path.exists()

    df = pd.read_csv(path)
    row = df.iloc[0]

    assert row["status"] == "waiting_for_labels"
    assert str(row["retraining_allowed"]).lower() == "false"


def test_production_promotion_guard_blocks_without_true_labels():
    path = Path("data/production_promotion_guard_v1.csv")
    assert path.exists()

    df = pd.read_csv(path)
    row = df.iloc[0]

    assert str(row["promotion_allowed"]).lower() == "false"
    assert row["status"] == "blocked_waiting_for_true_labels"
    assert "no_trainable_true_labels" in row["blockers"]


def test_true_outcome_resolver_waits_for_mature_windows():
    path = Path("data/true_outcome_resolver_summary_v1.csv")
    assert path.exists()

    df = pd.read_csv(path)
    row = df.iloc[0]

    assert int(row["resolved_labels"]) == 0
    assert int(row["trainable_labels"]) == 0
    assert row["status"] == "waiting_for_mature_windows"
