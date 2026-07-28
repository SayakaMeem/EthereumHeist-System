from pathlib import Path
import json
import time
import pandas as pd

from app.services.etherscan_service import fetch_address_transactions
from app.services.tpp_tracking_service import run_one_hop_tpp_tracking

BASE_DIR = Path(r"D:\EthereumHeist_System")
TX_DIR = BASE_DIR / "data" / "raw" / "transactions"
RESULT_DIR = BASE_DIR / "results" / "tracking"
RESULT_DIR.mkdir(parents=True, exist_ok=True)


def _clean_address(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def _address_files_exist(address: str) -> bool:
    address = address.lower().strip()

    normal_file = TX_DIR / f"{address}_normal.csv"
    internal_file = TX_DIR / f"{address}_internal.csv"
    erc20_file = TX_DIR / f"{address}_erc20.csv"

    return normal_file.exists() and internal_file.exists() and erc20_file.exists()


def _ensure_address_crawled(address: str):
    address = address.lower().strip()

    if _address_files_exist(address):
        return {
            "address": address,
            "status": "already_crawled"
        }

    result = fetch_address_transactions(address)

    return {
        "address": address,
        "status": "newly_crawled",
        "crawler_result": result
    }


def run_multi_hop_tpp_tracking(
    root_address: str,
    max_depth: int = 2,
    max_addresses_per_layer: int = 10,
    beta: float = 0.01,
    omega: int = 1000,
    crawl_missing: bool = True
):
    """
    Laptop-friendly multi-hop TPP tracking.

    root_address = placement/heist address
    max_depth = how many layers to track
    max_addresses_per_layer = maximum addresses to crawl/process per layer
    beta = dirty amount threshold
    omega = unknown service-provider transaction threshold
    crawl_missing = if True, crawl Etherscan when local transaction CSV is missing
    """

    root_address = root_address.lower().strip()

    visited = set()
    current_layer = {root_address}

    all_edges = []
    layer_records = []
    errors = []
    crawl_logs = []

    layer_records.append({
        "address": root_address,
        "layer": 0,
        "role": "placement"
    })

    for depth in range(0, max_depth + 1):
        if not current_layer:
            break

        limited_current_layer = list(current_layer)[:max_addresses_per_layer]
        next_layer = set()

        for address in limited_current_layer:
            address = address.lower().strip()

            if address in visited:
                continue

            visited.add(address)

            try:
                if crawl_missing:
                    crawl_result = _ensure_address_crawled(address)
                    crawl_logs.append(crawl_result)

                    # Slow down to avoid API rate issues
                    time.sleep(0.5)

                one_hop_result = run_one_hop_tpp_tracking(
                    address=address,
                    beta=beta,
                    omega=omega
                )

                output_file = Path(one_hop_result["output_file"])

                if output_file.exists():
                    df = pd.read_csv(output_file)

                    if not df.empty:
                        df["source_layer"] = depth
                        all_edges.append(df)

                        if "target" in df.columns and "label" in df.columns:
                            candidate_df = df[df["label"] == "candidate_layering"].copy()

                            candidate_df["target"] = candidate_df["target"].apply(_clean_address)

                            for target in candidate_df["target"].dropna().unique():
                                if target and target not in visited and target not in next_layer:
                                    if len(next_layer) < max_addresses_per_layer:
                                        next_layer.add(target)

                                        layer_records.append({
                                            "address": target,
                                            "layer": depth + 1,
                                            "role": "candidate_layering"
                                        })

                            integration_df = df[df["label"] == "integration_unknown_service"].copy()

                            if not integration_df.empty:
                                integration_df["target"] = integration_df["target"].apply(_clean_address)

                                for target in integration_df["target"].dropna().unique():
                                    layer_records.append({
                                        "address": target,
                                        "layer": depth + 1,
                                        "role": "integration_unknown_service"
                                    })

            except Exception as e:
                errors.append({
                    "address": address,
                    "layer": depth,
                    "error": str(e)
                })

        current_layer = next_layer

    if all_edges:
        edge_df = pd.concat(all_edges, ignore_index=True)
    else:
        edge_df = pd.DataFrame()

    layer_df = pd.DataFrame(layer_records)

    safe_root = root_address.replace("0x", "")

    edges_file = RESULT_DIR / f"{safe_root}_multihop_edges.csv"
    layers_file = RESULT_DIR / f"{safe_root}_multihop_layers.csv"
    summary_file = RESULT_DIR / f"{safe_root}_multihop_summary.json"

    edge_df.to_csv(edges_file, index=False)
    layer_df.to_csv(layers_file, index=False)

    summary = {
        "root_address": root_address,
        "max_depth": max_depth,
        "max_addresses_per_layer": max_addresses_per_layer,
        "beta": beta,
        "omega": omega,
        "visited_address_count": len(visited),
        "tracked_edge_count": int(len(edge_df)),
        "layer_address_count": int(len(layer_df)),
        "edges_file": str(edges_file),
        "layers_file": str(layers_file),
        "summary_file": str(summary_file),
        "errors": errors[:20],
        "crawl_logs_preview": crawl_logs[:10],
        "layer_preview": layer_df.head(20).to_dict(orient="records"),
    }

    summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return summary