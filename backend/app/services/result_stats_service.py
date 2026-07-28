from pathlib import Path
import pandas as pd

BASE_DIR = Path(r"D:\EthereumHeist_System")
TRACKING_DIR = BASE_DIR / "results" / "tracking"


def _safe_bool_series(series):
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def get_tracking_stats(edges_file_name: str):
    safe_file_name = Path(edges_file_name).name
    edges_path = TRACKING_DIR / safe_file_name

    if not edges_path.exists():
        return {
            "error": f"{safe_file_name} not found",
            "tracking_folder": str(TRACKING_DIR),
        }

    edges_df = pd.read_csv(edges_path)

    total_edges = int(len(edges_df))

    if "transaction_type" in edges_df.columns:
        transaction_type_counts = (
            edges_df["transaction_type"]
            .fillna("unknown")
            .astype(str)
            .value_counts()
            .to_dict()
        )
    else:
        transaction_type_counts = {"unknown": total_edges}

    if "label" in edges_df.columns:
        label_counts = (
            edges_df["label"]
            .fillna("unknown")
            .astype(str)
            .value_counts()
            .to_dict()
        )
    else:
        label_counts = {"unknown": total_edges}

    unique_source_addresses = (
        int(edges_df["source"].nunique()) if "source" in edges_df.columns else 0
    )

    unique_target_addresses = (
        int(edges_df["target"].nunique()) if "target" in edges_df.columns else 0
    )

    service_file_name = safe_file_name.replace(".csv", "_service_enriched.csv")
    service_path = TRACKING_DIR / service_file_name

    matched_service_edges = 0
    unique_service_providers = 0

    if service_path.exists():
        service_df = pd.read_csv(service_path)

        if "is_service_provider" in service_df.columns:
            matched_mask = _safe_bool_series(service_df["is_service_provider"])
            matched_service_edges = int(matched_mask.sum())

            if "target_clean" in service_df.columns:
                unique_service_providers = int(
                    service_df.loc[matched_mask, "target_clean"].nunique()
                )
            elif "target" in service_df.columns:
                unique_service_providers = int(
                    service_df.loc[matched_mask, "target"].nunique()
                )

    unmatched_service_edges = max(total_edges - matched_service_edges, 0)

    return {
        "edges_file": str(edges_path),
        "service_file": str(service_path) if service_path.exists() else "",
        "total_edges": total_edges,
        "unique_source_addresses": unique_source_addresses,
        "unique_target_addresses": unique_target_addresses,
        "transaction_type_counts": transaction_type_counts,
        "label_counts": label_counts,
        "matched_service_edges": matched_service_edges,
        "unmatched_service_edges": unmatched_service_edges,
        "unique_service_providers": unique_service_providers,
    }