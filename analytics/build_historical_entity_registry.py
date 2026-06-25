from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_COLUMNS = [
    "entity_id",
    "entity_type",
    "display_name",
    "canonical_name",
    "vendor",
    "status",
    "source_id",
    "notes",
]

ROWS = [
    {"entity_id": "vendor_amd", "entity_type": "vendor", "display_name": "AMD", "canonical_name": "Advanced Micro Devices", "vendor": "AMD", "status": "active", "source_id": "amd_ir", "notes": "Vendor entity."},
    {"entity_id": "vendor_intel", "entity_type": "vendor", "display_name": "Intel", "canonical_name": "Intel Corporation", "vendor": "Intel", "status": "active", "source_id": "intel_newsroom", "notes": "Vendor entity."},
    {"entity_id": "vendor_nvidia", "entity_type": "vendor", "display_name": "NVIDIA", "canonical_name": "NVIDIA Corporation", "vendor": "NVIDIA", "status": "active", "source_id": "nvidia_news", "notes": "Vendor entity."},

    {"entity_id": "arch_cdna", "entity_type": "architecture", "display_name": "CDNA", "canonical_name": "AMD CDNA", "vendor": "AMD", "status": "active", "source_id": "amd_products", "notes": "AMD datacenter GPU architecture family."},
    {"entity_id": "arch_cdna2", "entity_type": "architecture", "display_name": "CDNA2", "canonical_name": "AMD CDNA2", "vendor": "AMD", "status": "active", "source_id": "amd_products", "notes": "AMD datacenter GPU architecture family."},
    {"entity_id": "arch_cdna3", "entity_type": "architecture", "display_name": "CDNA3", "canonical_name": "AMD CDNA3", "vendor": "AMD", "status": "active", "source_id": "amd_products", "notes": "AMD datacenter GPU architecture family."},
    {"entity_id": "arch_ponte_vecchio", "entity_type": "architecture", "display_name": "Ponte Vecchio / Xe-HPC", "canonical_name": "Intel Ponte Vecchio Xe-HPC", "vendor": "Intel", "status": "active", "source_id": "intel_products", "notes": "Intel Data Center GPU Max architecture reference."},
    {"entity_id": "arch_gaudi2", "entity_type": "architecture", "display_name": "Gaudi2", "canonical_name": "Intel Gaudi2", "vendor": "Intel", "status": "active", "source_id": "intel_newsroom", "notes": "Intel Habana AI accelerator architecture reference."},
    {"entity_id": "arch_gaudi3", "entity_type": "architecture", "display_name": "Gaudi3", "canonical_name": "Intel Gaudi3", "vendor": "Intel", "status": "active", "source_id": "intel_newsroom", "notes": "Intel AI accelerator architecture reference."},

    {"entity_id": "api_rocm", "entity_type": "compute_api", "display_name": "ROCm", "canonical_name": "AMD ROCm", "vendor": "AMD", "status": "active", "source_id": "rocm_docs", "notes": "AMD open software stack for accelerated compute."},
    {"entity_id": "api_oneapi", "entity_type": "compute_api", "display_name": "oneAPI", "canonical_name": "Intel oneAPI", "vendor": "Intel", "status": "active", "source_id": "intel_products", "notes": "Intel cross-architecture programming model."},
    {"entity_id": "api_synapseai", "entity_type": "compute_api", "display_name": "SynapseAI", "canonical_name": "Intel Gaudi SynapseAI", "vendor": "Intel", "status": "active", "source_id": "intel_newsroom", "notes": "Software stack reference for Intel Gaudi accelerators."},
    {"entity_id": "api_cuda", "entity_type": "compute_api", "display_name": "CUDA", "canonical_name": "NVIDIA CUDA", "vendor": "NVIDIA", "status": "active", "source_id": "cuda_docs", "notes": "NVIDIA parallel computing platform and programming model."},

    {"entity_id": "family_amd_instinct", "entity_type": "product_family", "display_name": "AMD Instinct", "canonical_name": "AMD Instinct Accelerators", "vendor": "AMD", "status": "active", "source_id": "amd_products", "notes": "AMD datacenter accelerator product family."},
    {"entity_id": "family_intel_data_center_gpu_max", "entity_type": "product_family", "display_name": "Intel Data Center GPU Max", "canonical_name": "Intel Data Center GPU Max Series", "vendor": "Intel", "status": "active", "source_id": "intel_products", "notes": "Intel datacenter GPU product family."},
    {"entity_id": "family_intel_gaudi", "entity_type": "product_family", "display_name": "Intel Gaudi", "canonical_name": "Intel Gaudi AI Accelerators", "vendor": "Intel", "status": "active", "source_id": "intel_newsroom", "notes": "Intel Gaudi accelerator product family."},

    {"entity_id": "gpu_amd_instinct_mi100", "entity_type": "gpu", "display_name": "AMD Instinct MI100", "canonical_name": "AMD Instinct MI100", "vendor": "AMD", "status": "active", "source_id": "amd_ir", "notes": "Linked to AMD historical GPU registry."},
    {"entity_id": "gpu_amd_instinct_mi300x", "entity_type": "gpu", "display_name": "AMD Instinct MI300X", "canonical_name": "AMD Instinct MI300X", "vendor": "AMD", "status": "active", "source_id": "amd_ir", "notes": "Linked to AMD historical GPU registry."},
    {"entity_id": "gpu_intel_max_1100", "entity_type": "gpu", "display_name": "Intel Data Center GPU Max 1100", "canonical_name": "Intel Data Center GPU Max 1100", "vendor": "Intel", "status": "active", "source_id": "intel_products", "notes": "Linked to Intel historical GPU registry."},
    {"entity_id": "gpu_intel_gaudi2", "entity_type": "gpu", "display_name": "Intel Gaudi2", "canonical_name": "Intel Gaudi2", "vendor": "Intel", "status": "active", "source_id": "intel_newsroom", "notes": "Linked to Intel historical GPU registry."},
    {"entity_id": "gpu_intel_gaudi3", "entity_type": "gpu", "display_name": "Intel Gaudi 3 AI Accelerator", "canonical_name": "Intel Gaudi 3 AI Accelerator", "vendor": "Intel", "status": "active", "source_id": "intel_newsroom", "notes": "Linked to Intel historical GPU registry."},
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "historical_entity_registry.csv"
    warehouse_path = ROOT / "warehouse" / "historical" / "metadata" / "historical_entity_registry.csv"
    write_csv(data_path)
    write_csv(warehouse_path)
    print(f"Wrote {len(ROWS)} historical entity registry rows.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
