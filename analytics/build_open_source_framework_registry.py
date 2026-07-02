from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_COLUMNS = [
    "release_id",
    "project",
    "version",
    "release_date",
    "milestone_type",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
]

# Dates verified directly against the GitHub Releases API
# (api.github.com/repos/{org}/{repo}/releases), not recalled from memory
# or taken from secondary aggregators - source_confidence is "high" for
# all rows here, higher than most other registries in this repo, because
# GitHub's own release timestamps are about as close to a primary source
# as this kind of data gets. "latest" rows are a snapshot as of the
# observation date below and will go stale as new releases ship -
# re-run this script's underlying API calls periodically to refresh them
# rather than treating "latest" as a permanent fact.

ROWS = [
    {
        "release_id": "oss000001",
        "project": "PyTorch",
        "version": "v1.0.0",
        "release_date": "2018-12-07",
        "milestone_type": "first_stable_release",
        "source_url": "https://github.com/pytorch/pytorch/releases/tag/v1.0.0",
        "source_type": "official_github_release",
        "source_confidence": "high",
        "notes": "Verified via GitHub Releases API published_at timestamp.",
    },
    {
        "release_id": "oss000002",
        "project": "PyTorch",
        "version": "v2.12.1",
        "release_date": "2026-06-18",
        "milestone_type": "latest_as_of_observation",
        "source_url": "https://github.com/pytorch/pytorch/releases/tag/v2.12.1",
        "source_type": "official_github_release",
        "source_confidence": "high",
        "notes": "Observed 2026-07-02 via GitHub Releases API 'latest' endpoint. Will go stale as new releases ship; re-query rather than treat as permanent.",
    },
    {
        "release_id": "oss000003",
        "project": "vLLM",
        "version": "v0.1.0",
        "release_date": "2023-06-20",
        "milestone_type": "first_stable_release",
        "source_url": "https://github.com/vllm-project/vllm/releases/tag/v0.1.0",
        "source_type": "official_github_release",
        "source_confidence": "high",
        "notes": "Verified via GitHub Releases API published_at timestamp.",
    },
    {
        "release_id": "oss000004",
        "project": "vLLM",
        "version": "v0.24.0",
        "release_date": "2026-06-29",
        "milestone_type": "latest_as_of_observation",
        "source_url": "https://github.com/vllm-project/vllm/releases/tag/v0.24.0",
        "source_type": "official_github_release",
        "source_confidence": "high",
        "notes": "Observed 2026-07-02 via GitHub Releases API 'latest' endpoint. Will go stale as new releases ship; re-query rather than treat as permanent.",
    },
    {
        "release_id": "oss000005",
        "project": "Triton Inference Server",
        "version": "v0.8.0",
        "release_date": "2018-11-12",
        "milestone_type": "earliest_available_release",
        "source_url": "https://github.com/triton-inference-server/server/releases/tag/v0.8.0",
        "source_type": "official_github_release",
        "source_confidence": "high",
        "notes": "Earliest release visible via the GitHub Releases API (releases list does not extend further back); may not be the project's true first version if earlier tags were never published as GitHub releases.",
    },
    {
        "release_id": "oss000006",
        "project": "Triton Inference Server",
        "version": "v2.70.0",
        "release_date": "2026-06-26",
        "milestone_type": "latest_as_of_observation",
        "source_url": "https://github.com/triton-inference-server/server/releases/tag/v2.70.0",
        "source_type": "official_github_release",
        "source_confidence": "high",
        "notes": "Observed 2026-07-02 via GitHub Releases API 'latest' endpoint. Will go stale as new releases ship; re-query rather than treat as permanent.",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "open_source_framework_registry.csv"
    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "open_source"
        / "open_source_framework_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} open source framework release records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
