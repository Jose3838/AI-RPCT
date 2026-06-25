from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_package_scaffold_exists():
    expected = [
        "airpct",
        "airpct/builders",
        "airpct/analytics",
        "airpct/governance",
        "airpct/forecasting",
        "airpct/registries",
        "airpct/dashboard",
    ]

    for path in expected:
        assert (ROOT / path).exists()


def test_package_init_files_exist():
    expected = [
        "airpct/__init__.py",
        "airpct/builders/__init__.py",
        "airpct/analytics/__init__.py",
        "airpct/governance/__init__.py",
        "airpct/forecasting/__init__.py",
        "airpct/registries/__init__.py",
        "airpct/dashboard/__init__.py",
    ]

    for path in expected:
        assert (ROOT / path).exists()
