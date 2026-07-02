from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_COLUMNS = [
    "performance_record_id",
    "gpu_id",
    "vendor_registry",
    "vendor",
    "product_name",
    "peak_fp32_tflops",
    "peak_fp16_tflops",
    "sparsity_note",
    "memory_bandwidth_gbps",
    "memory_capacity_gb",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
]

# gpu_id values match each vendor's own historical GPU registry primary key
# (amd/intel registries use "gpu_id", the nvidia registry uses "entity_id")
# rather than historical_entity_registry.csv's ids, which use a different,
# inconsistent naming convention (pre-existing mismatch, not fixed here).

ROWS = [
    {
        "performance_record_id": "perf000001",
        "gpu_id": "gpu_nvidia_tesla_k80",
        "vendor_registry": "nvidia_historical_gpu_registry",
        "vendor": "NVIDIA",
        "product_name": "Tesla K80",
        "peak_fp32_tflops": "5.6",
        "peak_fp16_tflops": "",
        "sparsity_note": "dual-GPU board, combined figure; no FP16 tensor cores (pre-Volta)",
        "memory_bandwidth_gbps": "480",
        "memory_capacity_gb": "24",
        "source_url": "https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/TeslaK80-datasheet.pdf",
        "source_type": "official_datasheet",
        "source_confidence": "medium",
        "notes": "Figures widely repeated across secondary sources citing the official K80 datasheet; not independently re-verified against the raw PDF text.",
    },
    {
        "performance_record_id": "perf000002",
        "gpu_id": "gpu_nvidia_v100",
        "vendor_registry": "nvidia_historical_gpu_registry",
        "vendor": "NVIDIA",
        "product_name": "Tesla V100",
        "peak_fp32_tflops": "15.7",
        "peak_fp16_tflops": "125",
        "sparsity_note": "dense, no sparsity (Volta predates structured sparsity support)",
        "memory_bandwidth_gbps": "900",
        "memory_capacity_gb": "16 / 32",
        "source_url": "https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf",
        "source_type": "official_datasheet",
        "source_confidence": "medium",
        "notes": "SXM2 variant. PCIe variant is clocked lower; not recorded separately here.",
    },
    {
        "performance_record_id": "perf000003",
        "gpu_id": "gpu_nvidia_a100",
        "vendor_registry": "nvidia_historical_gpu_registry",
        "vendor": "NVIDIA",
        "product_name": "A100",
        "peak_fp32_tflops": "19.5",
        "peak_fp16_tflops": "312",
        "sparsity_note": "dense (624 with 2:4 structured sparsity)",
        "memory_bandwidth_gbps": "2039",
        "memory_capacity_gb": "40 / 80",
        "source_url": "https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-nvidia-us-2188504-web.pdf",
        "source_type": "official_datasheet",
        "source_confidence": "medium",
        "notes": "80GB SXM variant bandwidth shown; 40GB and PCIe variants differ.",
    },
    {
        "performance_record_id": "perf000004",
        "gpu_id": "gpu_nvidia_h100",
        "vendor_registry": "nvidia_historical_gpu_registry",
        "vendor": "NVIDIA",
        "product_name": "H100",
        "peak_fp32_tflops": "67",
        "peak_fp16_tflops": "989",
        "sparsity_note": "dense, SXM5 (1979 with 2:4 structured sparsity)",
        "memory_bandwidth_gbps": "3350",
        "memory_capacity_gb": "80",
        "source_url": "https://www.nvidia.com/en-us/data-center/h100/",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "SXM5 variant. PCIe variant has lower TDP/clocks and ~2000 GB/s bandwidth; not recorded separately here.",
    },
    {
        "performance_record_id": "perf000005",
        "gpu_id": "gpu_nvidia_b200",
        "vendor_registry": "nvidia_historical_gpu_registry",
        "vendor": "NVIDIA",
        "product_name": "B200",
        "peak_fp32_tflops": "",
        "peak_fp16_tflops": "2250",
        "sparsity_note": "dense (4500 with 2:4 structured sparsity)",
        "memory_bandwidth_gbps": "8000",
        "memory_capacity_gb": "180",
        "source_url": "https://www.nvidia.com/en-us/data-center/dgx-b200/",
        "source_type": "secondary_aggregated",
        "source_confidence": "low",
        "notes": "Blackwell generation; secondary sources show some variance in exact memory capacity (180GB vs 192GB) and bandwidth (7.7-8 TB/s) depending on SKU/config. Lower confidence than older, more extensively cross-checked generations.",
    },
    {
        "performance_record_id": "perf000006",
        "gpu_id": "amd-instinct-mi100",
        "vendor_registry": "amd_historical_gpu_registry",
        "vendor": "AMD",
        "product_name": "AMD Instinct MI100",
        "peak_fp32_tflops": "11.5",
        "peak_fp16_tflops": "184.6",
        "sparsity_note": "peak matrix/tensor FP16 reported up to ~383 TFLOPS in some sources; vector FP16 figure used here",
        "memory_bandwidth_gbps": "1229",
        "memory_capacity_gb": "32",
        "source_url": "https://www.amd.com/en/products/accelerators/instinct/mi100.html",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "CDNA architecture. Matrix-core peak figure differs from vector FP16 figure; see sparsity_note.",
    },
    {
        "performance_record_id": "perf000007",
        "gpu_id": "amd-instinct-mi210",
        "vendor_registry": "amd_historical_gpu_registry",
        "vendor": "AMD",
        "product_name": "AMD Instinct MI210",
        "peak_fp32_tflops": "22.6",
        "peak_fp16_tflops": "181",
        "sparsity_note": "dense matrix FP16/BF16, no sparsity",
        "memory_bandwidth_gbps": "1600",
        "memory_capacity_gb": "64",
        "source_url": "https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/product-briefs/instinct-mi210-brochure.pdf",
        "source_type": "official_datasheet",
        "source_confidence": "medium",
        "notes": "CDNA2 architecture. FP32 vector figure (23 TFLOPS) and FP32 matrix figure (45 TFLOPS) both appear in vendor materials; vector figure used here.",
    },
    {
        "performance_record_id": "perf000008",
        "gpu_id": "amd-instinct-mi300x",
        "vendor_registry": "amd_historical_gpu_registry",
        "vendor": "AMD",
        "product_name": "AMD Instinct MI300X",
        "peak_fp32_tflops": "",
        "peak_fp16_tflops": "1307.4",
        "sparsity_note": "dense (2614.9 with sparsity)",
        "memory_bandwidth_gbps": "5300",
        "memory_capacity_gb": "192",
        "source_url": "https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-data-sheet.pdf",
        "source_type": "official_datasheet",
        "source_confidence": "medium",
        "notes": "CDNA3 architecture. Positioned by AMD as an H100 competitor; widely cross-referenced 192GB/5.3TB/s figures.",
    },
    {
        "performance_record_id": "perf000009",
        "gpu_id": "intel-data-center-gpu-max-1100",
        "vendor_registry": "intel_historical_gpu_registry",
        "vendor": "Intel",
        "product_name": "Intel Data Center GPU Max 1100",
        "peak_fp32_tflops": "21.8",
        "peak_fp16_tflops": "",
        "sparsity_note": "vector FP32 figure; Xe Matrix Engine (XMX) BF16/FP16 figures not consistently reported for this specific SKU vs. the higher-end Max 1550 OAM card",
        "memory_bandwidth_gbps": "1229",
        "memory_capacity_gb": "48",
        "source_url": "https://www.intel.com/content/www/us/en/products/sku/232876/intel-data-center-gpu-max-1100/specifications.html",
        "source_type": "secondary_aggregated",
        "source_confidence": "low",
        "notes": "Direct fetch of Intel's own spec page was blocked (403); figures sourced via a secondary GPU-database aggregator citing that page. Lower confidence than directly-verified official sources.",
    },
    {
        "performance_record_id": "perf000010",
        "gpu_id": "intel-gaudi2",
        "vendor_registry": "intel_historical_gpu_registry",
        "vendor": "Intel",
        "product_name": "Intel Gaudi2",
        "peak_fp32_tflops": "",
        "peak_fp16_tflops": "",
        "sparsity_note": "",
        "memory_bandwidth_gbps": "2450",
        "memory_capacity_gb": "96",
        "source_url": "https://download.intel.com/newsroom/2022/corporate/vision/Habana-Gaudi2-Launch-Fact-Sheet.pdf",
        "source_type": "secondary_aggregated",
        "source_confidence": "low",
        "notes": "Intel does not publish Gaudi2 compute performance in directly comparable dense-TFLOPS terms the way NVIDIA/AMD do (marketing relies on MLPerf benchmark results instead). TFLOPS fields deliberately left blank rather than estimated; memory bandwidth/capacity only.",
    },
    {
        "performance_record_id": "perf000011",
        "gpu_id": "intel-gaudi3-launch",
        "vendor_registry": "intel_historical_gpu_registry",
        "vendor": "Intel",
        "product_name": "Intel Gaudi 3 AI Accelerator",
        "peak_fp32_tflops": "",
        "peak_fp16_tflops": "1800",
        "sparsity_note": "BF16/FP8 matrix compute, reported as ~1.8 PFLOPS by Intel; precision/sparsity basis not fully disclosed in the same terms NVIDIA/AMD use",
        "memory_bandwidth_gbps": "3700",
        "memory_capacity_gb": "128",
        "source_url": "https://newsroom.intel.com/artificial-intelligence/next-generation-ai-solutions-xeon-6-gaudi-3",
        "source_type": "secondary_aggregated",
        "source_confidence": "low",
        "notes": "Figure not directly comparable to NVIDIA/AMD dense-TFLOPS figures without knowing Intel's exact precision/sparsity assumptions; treat as directional only.",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "historical_performance_registry.csv"
    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "performance"
        / "historical_performance_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} historical performance registry rows.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
