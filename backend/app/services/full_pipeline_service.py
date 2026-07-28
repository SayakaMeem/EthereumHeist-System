from pathlib import Path
import time
import traceback

from app.services.multi_hop_tracking_service import run_multi_hop_tpp_tracking
from app.services.service_provider_matching_service import enrich_edges_with_service_providers
from app.services.risk_scoring_service import add_risk_scores_to_edges
from app.services.graph_service import build_tracking_graph

BASE_DIR = Path(r"D:\EthereumHeist_System")
TRACKING_DIR = BASE_DIR / "results" / "tracking"


def _get_edges_file_name(tracking_result):
    possible_keys = [
        "edges_file_name",
        "edges_file",
        "output_edges_file",
        "multihop_edges_file",
    ]

    for key in possible_keys:
        value = tracking_result.get(key)
        if value:
            return Path(value).name

    output_files = tracking_result.get("output_files", {})
    if isinstance(output_files, dict):
        for key in possible_keys:
            value = output_files.get(key)
            if value:
                return Path(value).name

    # fallback: find newest multihop edges file
    files = sorted(
        TRACKING_DIR.glob("*_multihop_edges.csv"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if files:
        return files[0].name

    return None


def run_full_aml_pipeline(
    address: str,
    max_depth: int = 2,
    max_addresses_per_layer: int = 3,
    beta: float = 0.01,
    omega: int = 1000,
    crawl_missing: bool = False,
):
    start_time = time.time()

    try:
        # Use positional address to avoid parameter-name mismatch
        tracking_result = run_multi_hop_tpp_tracking(
            address,
            max_depth=max_depth,
            max_addresses_per_layer=max_addresses_per_layer,
            beta=beta,
            omega=omega,
            crawl_missing=crawl_missing,
        )

        if not isinstance(tracking_result, dict):
            return {
                "error": "Tracking result is not a dictionary",
                "tracking_result_type": str(type(tracking_result)),
                "tracking_result": str(tracking_result),
            }

        if "error" in tracking_result:
            return {
                "error": "Multi-hop tracking failed",
                "details": tracking_result,
            }

        edges_file = _get_edges_file_name(tracking_result)

        if not edges_file:
            return {
                "error": "Edges file name not found after tracking",
                "tracking_result": tracking_result,
            }

        service_result = enrich_edges_with_service_providers(edges_file)

        service_enriched_file = Path(
            service_result.get("output_file", edges_file)
        ).name

        risk_result = add_risk_scores_to_edges(service_enriched_file)

        try:
            graph_result = build_tracking_graph(edges_file, limit=300)
        except TypeError:
            graph_result = build_tracking_graph(edges_file)

        end_time = time.time()

        return {
            "status": "success",
            "address": address,
            "max_depth": max_depth,
            "max_addresses_per_layer": max_addresses_per_layer,
            "beta": beta,
            "omega": omega,
            "crawl_missing": crawl_missing,
            "runtime_seconds": round(end_time - start_time, 3),
            "edges_file_used": edges_file,
            "service_enriched_file": service_enriched_file,
            "tracking_result": tracking_result,
            "service_provider_result": service_result,
            "risk_result": risk_result,
            "graph_result": graph_result,
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "traceback": traceback.format_exc(),
        }