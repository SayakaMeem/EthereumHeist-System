from pathlib import Path
import json
import pandas as pd

from app.services.multi_hop_tracking_service import run_multi_hop_tpp_tracking
from app.services.service_provider_matching_service import enrich_edges_with_service_providers

BASE_DIR = Path(r"D:\EthereumHeist_System")
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
EXPERIMENT_DIR = BASE_DIR / "results" / "experiments"
EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)


def _find_file(filename: str) -> Path:
    matches = list(RAW_DATA_DIR.rglob(filename))

    if not matches:
        raise FileNotFoundError(f"{filename} not found inside {RAW_DATA_DIR}")

    return matches[0]


def _clean_address(value):
    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def _find_address_from_row(row):
    for col, value in row.items():
        col_lower = str(col).lower()
        value_str = _clean_address(value)

        if (
            "address" in col_lower
            or "account" in col_lower
            or "wallet" in col_lower
        ) and value_str.startswith("0x"):
            return value_str

    for _, value in row.items():
        value_str = _clean_address(value)

        if value_str.startswith("0x") and len(value_str) >= 40:
            return value_str

    return ""


def _find_label_from_row(row):
    for col, value in row.items():
        col_lower = str(col).lower()

        if (
            "heist" in col_lower
            or "event" in col_lower
            or "name" in col_lower
            or "label" in col_lower
        ):
            label = str(value).strip()

            if label:
                return label

    return "Unknown Heist"


def _is_bad_label(label: str):
    if not label:
        return True

    cleaned = str(label).strip()

    if cleaned == "":
        return True

    bad_values = {
        "?",
        "??",
        "? ? ?",
        "unknown",
        "unknown heist",
        "nan",
        "none",
        "null",
    }

    if cleaned.lower() in bad_values:
        return True

    alnum_count = sum(ch.isalnum() for ch in cleaned)

    if alnum_count < 2:
        return True

    return False


def run_batch_experiment(
    limit: int = 5,
    max_depth: int = 1,
    max_addresses_per_layer: int = 1,
    beta: float = 0.01,
    omega: int = 1000,
    crawl_missing: bool = False,
):
    label_path = _find_file("Heist label-etherscan.csv")
    label_df = pd.read_csv(label_path)

    results = []
    used_addresses = set()

    for _, row in label_df.iterrows():
        if len(results) >= limit:
            break

        address = _find_address_from_row(row)

        if not address:
            continue

        if address in used_addresses:
            continue

        used_addresses.add(address)

        heist_label = _find_label_from_row(row)

        if _is_bad_label(heist_label):
            heist_label = f"Heist {len(results) + 1} ({address[:8]}...{address[-6:]})"

        experiment_row = {
            "heist_label": heist_label,
            "address": address,
            "status": "failed",
            "visited_address_count": 0,
            "tracked_edge_count": 0,
            "layer_address_count": 0,
            "matched_service_provider_edges": 0,
            "unique_service_providers": 0,
            "max_depth": max_depth,
            "max_addresses_per_layer": max_addresses_per_layer,
            "crawl_missing": crawl_missing,
            "edges_file": "",
            "layers_file": "",
            "summary_file": "",
            "service_file": "",
            "error": "",
        }

        try:
            tracking_summary = run_multi_hop_tpp_tracking(
                root_address=address,
                max_depth=max_depth,
                max_addresses_per_layer=max_addresses_per_layer,
                beta=beta,
                omega=omega,
                crawl_missing=crawl_missing,
            )

            experiment_row["status"] = "success"
            experiment_row["visited_address_count"] = tracking_summary.get(
                "visited_address_count", 0
            )
            experiment_row["tracked_edge_count"] = tracking_summary.get(
                "tracked_edge_count", 0
            )
            experiment_row["layer_address_count"] = tracking_summary.get(
                "layer_address_count", 0
            )
            experiment_row["edges_file"] = tracking_summary.get("edges_file", "")
            experiment_row["layers_file"] = tracking_summary.get("layers_file", "")
            experiment_row["summary_file"] = tracking_summary.get("summary_file", "")

            edges_file_path = tracking_summary.get("edges_file", "")
            edges_file_name = Path(edges_file_path).name if edges_file_path else ""

            if tracking_summary.get("tracked_edge_count", 0) > 0 and edges_file_name:
                service_result = enrich_edges_with_service_providers(edges_file_name)

                experiment_row["matched_service_provider_edges"] = service_result.get(
                    "matched_service_provider_edges", 0
                )
                experiment_row["unique_service_providers"] = service_result.get(
                    "unique_service_providers", 0
                )
                experiment_row["service_file"] = service_result.get("output_file", "")

        except Exception as e:
            experiment_row["status"] = "failed"
            experiment_row["error"] = str(e)

        results.append(experiment_row)

    result_df = pd.DataFrame(results)

    if not result_df.empty:
        successful_runs = int((result_df["status"] == "success").sum())
        failed_runs = int((result_df["status"] == "failed").sum())

        total_tracked_edges = int(result_df["tracked_edge_count"].sum())
        average_tracked_edges = round(float(result_df["tracked_edge_count"].mean()), 2)
        max_tracked_edges = int(result_df["tracked_edge_count"].max())

        total_layer_addresses = int(result_df["layer_address_count"].sum())
        average_layer_addresses = round(float(result_df["layer_address_count"].mean()), 2)

        total_service_matches = int(result_df["matched_service_provider_edges"].sum())
        average_service_matches = round(
            float(result_df["matched_service_provider_edges"].mean()), 2
        )

        total_unique_service_providers = int(result_df["unique_service_providers"].sum())
    else:
        successful_runs = 0
        failed_runs = 0

        total_tracked_edges = 0
        average_tracked_edges = 0
        max_tracked_edges = 0

        total_layer_addresses = 0
        average_layer_addresses = 0

        total_service_matches = 0
        average_service_matches = 0
        total_unique_service_providers = 0

    output_csv = EXPERIMENT_DIR / "experiment_result.csv"
    output_json = EXPERIMENT_DIR / "experiment_result.json"

    result_df.to_csv(output_csv, index=False)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return {
        "experiment_status": "completed",
        "input_label_file": str(label_path),
        "limit": limit,
        "total_experiments": len(results),
        "successful_runs": successful_runs,
        "failed_runs": failed_runs,
        "total_tracked_edges": total_tracked_edges,
        "average_tracked_edges": average_tracked_edges,
        "max_tracked_edges": max_tracked_edges,
        "total_layer_addresses": total_layer_addresses,
        "average_layer_addresses": average_layer_addresses,
        "total_service_matches": total_service_matches,
        "average_service_matches": average_service_matches,
        "total_unique_service_providers": total_unique_service_providers,
        "output_csv": str(output_csv),
        "output_json": str(output_json),
        "preview": result_df.head(20).fillna("").to_dict(orient="records"),
    }


def list_experiment_files():
    EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)

    files = []

    for file in EXPERIMENT_DIR.glob("*"):
        if file.is_file():
            files.append(
                {
                    "file_name": file.name,
                    "path": str(file),
                    "size_kb": round(file.stat().st_size / 1024, 2),
                    "extension": file.suffix.lower(),
                }
            )

    return {
        "experiment_folder": str(EXPERIMENT_DIR),
        "file_count": len(files),
        "files": files,
    }


def preview_experiment_csv(file_name: str):
    safe_file_name = Path(file_name).name
    file_path = EXPERIMENT_DIR / safe_file_name

    if not file_path.exists():
        return {
            "error": f"{safe_file_name} not found",
            "experiment_folder": str(EXPERIMENT_DIR),
        }

    df = pd.read_csv(file_path)

    return {
        "file_name": safe_file_name,
        "rows": int(len(df)),
        "columns": list(df.columns),
        "preview": df.head(50).fillna("").to_dict(orient="records"),
    }