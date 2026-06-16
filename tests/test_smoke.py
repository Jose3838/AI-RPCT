from pathlib import Path

def test_core_files_exist():
    assert Path("main.py").exists()
    assert Path("api/routes.py").exists()
    assert Path("run_daily.sh").exists()
    assert Path("README.md").exists()
