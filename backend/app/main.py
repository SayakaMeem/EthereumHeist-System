from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse

from app.config import TRACKING_DIR, ensure_directories
from app.services.dataset_service import get_dataset_status
from app.services.etherscan_service import fetch_address_transactions
from app.services.experiment_service import (
    list_experiment_files,
    preview_experiment_csv,
    run_batch_experiment,
)
from app.services.full_pipeline_service import run_full_aml_pipeline
from app.services.graph_service import build_tracking_graph
from app.services.incident_service import (
    get_dataset_overview,
    get_heist_events,
    get_heist_labels,
    get_service_provider_map,
)
from app.services.multi_hop_tracking_service import run_multi_hop_tpp_tracking
from app.services.result_stats_service import get_tracking_stats
from app.services.risk_scoring_service import add_risk_scores_to_edges
from app.services.service_provider_matching_service import (
    enrich_edges_with_service_providers,
)
from app.services.tpp_tracking_service import run_one_hop_tpp_tracking
from app.services.tracking_result_service import (
    list_tracking_files,
    preview_tracking_csv,
    preview_tracking_file,
    read_tracking_summary,
)
from app.services.transaction_service import (
    list_transaction_files,
    preview_transaction_file,
)

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("ethereumheist")


# ---------------------------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------------------------

def get_comma_separated_env(
    variable_name: str,
    default: str,
) -> list[str]:
    """
    Read a comma-separated environment variable and return cleaned values.

    Example:
        FRONTEND_ORIGINS=https://example.vercel.app,http://localhost:3000
    """
    raw_value = os.getenv(variable_name, default)

    return [
        item.strip()
        for item in raw_value.split(",")
        if item.strip()
    ]


APP_ENV = os.getenv("APP_ENV", "development").lower()

FRONTEND_ORIGINS = get_comma_separated_env(
    "FRONTEND_ORIGINS",
    (
        "http://localhost:3000,"
        "http://127.0.0.1:3000,"
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    ),
)

ALLOWED_HOSTS = get_comma_separated_env(
    "ALLOWED_HOSTS",
    "*",
)


# ---------------------------------------------------------------------------
# Application lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Run application startup and shutdown operations.
    """
    logger.info("Starting EthereumHeist AML backend")
    logger.info("Application environment: %s", APP_ENV)
    logger.info("Tracking directory: %s", TRACKING_DIR)

    ensure_directories()

    yield

    logger.info("Shutting down EthereumHeist AML backend")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="EthereumHeist AML System",
    description=(
        "API for Ethereum transaction collection, TPP tracking, "
        "multi-hop analysis, graph generation, experiment execution, "
        "service-provider matching, and AML risk scoring."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=ALLOWED_HOSTS,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)


# ---------------------------------------------------------------------------
# Basic routes
# ---------------------------------------------------------------------------

@app.get(
    "/",
    tags=["System"],
    summary="Backend home",
)
def home() -> dict[str, str]:
    return {
        "message": "EthereumHeist AML backend is running",
        "status": "online",
        "environment": APP_ENV,
        "docs": "/docs",
    }


@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
)
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "backend": "FastAPI",
        "environment": APP_ENV,
    }


@app.get(
    "/api/health",
    tags=["System"],
    summary="API health check",
)
def api_health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "ethereumheist-backend",
        "environment": APP_ENV,
    }


# ---------------------------------------------------------------------------
# Dataset routes
# ---------------------------------------------------------------------------

@app.get(
    "/dataset/status",
    tags=["Dataset"],
    summary="Get dataset status",
)
def dataset_status() -> Any:
    return get_dataset_status()


@app.get(
    "/dataset/overview",
    tags=["Dataset"],
    summary="Get dataset overview",
)
def dataset_overview() -> Any:
    return get_dataset_overview()


@app.get(
    "/incidents",
    tags=["Dataset"],
    summary="Get heist incidents",
)
def incidents() -> Any:
    return get_heist_events()


@app.get(
    "/heist-labels",
    tags=["Dataset"],
    summary="Get heist address labels",
)
def heist_labels() -> Any:
    return get_heist_labels()


@app.get(
    "/service-providers",
    tags=["Dataset"],
    summary="Get service-provider mappings",
)
def service_providers() -> Any:
    return get_service_provider_map()


# ---------------------------------------------------------------------------
# Etherscan crawling routes
# ---------------------------------------------------------------------------

@app.get(
    "/crawl/address/{address}",
    tags=["Crawling"],
    summary="Fetch transactions for an Ethereum address",
)
def crawl_address(address: str) -> Any:
    cleaned_address = address.strip()

    if not cleaned_address:
        raise HTTPException(
            status_code=400,
            detail="Ethereum address cannot be empty.",
        )

    return fetch_address_transactions(cleaned_address)


# ---------------------------------------------------------------------------
# Transaction routes
# ---------------------------------------------------------------------------

@app.get(
    "/transactions/files",
    tags=["Transactions"],
    summary="List transaction files",
)
def transaction_files() -> Any:
    return list_transaction_files()


@app.get(
    "/transactions/preview/{file_name}",
    tags=["Transactions"],
    summary="Preview a transaction file",
)
def transaction_preview(file_name: str) -> Any:
    return preview_transaction_file(file_name)


# ---------------------------------------------------------------------------
# Tracking routes
# ---------------------------------------------------------------------------

@app.get(
    "/track/one-hop/{address}",
    tags=["Tracking"],
    summary="Run one-hop TPP tracking",
)
def track_one_hop(
    address: str,
    beta: float = Query(
        default=0.01,
        ge=0.0,
        description="Minimum proportional-value threshold.",
    ),
    omega: int = Query(
        default=1000,
        ge=1,
        description="Maximum transaction/time constraint.",
    ),
) -> Any:
    return run_one_hop_tpp_tracking(
        address.strip(),
        beta,
        omega,
    )


@app.get(
    "/track/multi-hop/{address}",
    tags=["Tracking"],
    summary="Run multi-hop TPP tracking",
)
def track_multi_hop(
    address: str,
    max_depth: int = Query(
        default=2,
        ge=1,
        le=10,
        description="Maximum tracking depth.",
    ),
    max_addresses_per_layer: int = Query(
        default=10,
        ge=1,
        le=1000,
        description="Maximum addresses expanded at each layer.",
    ),
    beta: float = Query(
        default=0.01,
        ge=0.0,
        description="Minimum proportional-value threshold.",
    ),
    omega: int = Query(
        default=1000,
        ge=1,
        description="Maximum transaction/time constraint.",
    ),
    crawl_missing: bool = Query(
        default=True,
        description="Fetch missing transaction data when necessary.",
    ),
) -> Any:
    return run_multi_hop_tpp_tracking(
        root_address=address.strip(),
        max_depth=max_depth,
        max_addresses_per_layer=max_addresses_per_layer,
        beta=beta,
        omega=omega,
        crawl_missing=crawl_missing,
    )


@app.get(
    "/tracking/files",
    tags=["Tracking Results"],
    summary="List tracking-result files",
)
def tracking_files() -> Any:
    return list_tracking_files()


@app.get(
    "/tracking/preview/{file_name}",
    tags=["Tracking Results"],
    summary="Preview a tracking-result file",
)
def tracking_preview(file_name: str) -> Any:
    return preview_tracking_file(file_name)


@app.get(
    "/tracking/csv/{file_name}",
    tags=["Tracking Results"],
    summary="Preview a tracking CSV file",
)
def tracking_csv(file_name: str) -> Any:
    return preview_tracking_csv(file_name)


@app.get(
    "/tracking/summary/{file_name}",
    tags=["Tracking Results"],
    summary="Read a tracking summary",
)
def tracking_summary(file_name: str) -> Any:
    return read_tracking_summary(file_name)


@app.get(
    "/tracking/download/{file_name}",
    tags=["Tracking Results"],
    summary="Download a tracking-result file",
)
def download_tracking_file(file_name: str) -> FileResponse:
    safe_file_name = Path(file_name).name
    file_path = (TRACKING_DIR / safe_file_name).resolve()
    tracking_directory = TRACKING_DIR.resolve()

    try:
        file_path.relative_to(tracking_directory)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid file path.",
        ) from exc

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Tracking file '{safe_file_name}' was not found.",
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=400,
            detail="The requested path is not a file.",
        )

    return FileResponse(
        path=str(file_path),
        filename=safe_file_name,
        media_type="application/octet-stream",
    )


@app.get(
    "/tracking/enrich-service/{edges_file_name}",
    tags=["Tracking Results"],
    summary="Match tracking edges with service providers",
)
def enrich_service(edges_file_name: str) -> Any:
    return enrich_edges_with_service_providers(edges_file_name)


@app.get(
    "/tracking/stats/{edges_file_name}",
    tags=["Tracking Results"],
    summary="Get tracking statistics",
)
def tracking_stats(edges_file_name: str) -> Any:
    return get_tracking_stats(edges_file_name)


# ---------------------------------------------------------------------------
# Graph routes
# ---------------------------------------------------------------------------

@app.get(
    "/graph/tracking/{file_name}",
    tags=["Graph"],
    summary="Build a tracking graph",
)
def tracking_graph(
    file_name: str,
    limit: int = Query(
        default=30,
        ge=1,
        le=5000,
        description="Maximum number of graph records.",
    ),
) -> Any:
    return build_tracking_graph(file_name, limit)


# ---------------------------------------------------------------------------
# Experiment routes
# ---------------------------------------------------------------------------

@app.get(
    "/experiment/run",
    tags=["Experiments"],
    summary="Run a batch experiment",
)
def experiment_run(
    limit: int = Query(
        default=5,
        ge=1,
        le=1000,
    ),
    max_depth: int = Query(
        default=1,
        ge=1,
        le=10,
    ),
    max_addresses_per_layer: int = Query(
        default=1,
        ge=1,
        le=1000,
    ),
    beta: float = Query(
        default=0.01,
        ge=0.0,
    ),
    omega: int = Query(
        default=1000,
        ge=1,
    ),
    crawl_missing: bool = Query(default=False),
) -> Any:
    return run_batch_experiment(
        limit=limit,
        max_depth=max_depth,
        max_addresses_per_layer=max_addresses_per_layer,
        beta=beta,
        omega=omega,
        crawl_missing=crawl_missing,
    )


@app.get(
    "/experiment/files",
    tags=["Experiments"],
    summary="List experiment files",
)
def experiment_files() -> Any:
    return list_experiment_files()


@app.get(
    "/experiment/csv/{file_name}",
    tags=["Experiments"],
    summary="Preview an experiment CSV file",
)
def experiment_csv(file_name: str) -> Any:
    return preview_experiment_csv(file_name)


# ---------------------------------------------------------------------------
# Risk scoring routes
# ---------------------------------------------------------------------------

@app.get(
    "/risk/edges/{file_name}",
    tags=["Risk Scoring"],
    summary="Add AML risk scores to tracking edges",
)
def risk_edges(file_name: str) -> Any:
    return add_risk_scores_to_edges(file_name)


# ---------------------------------------------------------------------------
# Full pipeline route
# ---------------------------------------------------------------------------

@app.get(
    "/pipeline/full/{address}",
    tags=["Pipeline"],
    summary="Run the complete AML pipeline",
)
def full_pipeline(
    address: str,
    max_depth: int = Query(
        default=2,
        ge=1,
        le=10,
    ),
    max_addresses_per_layer: int = Query(
        default=3,
        ge=1,
        le=1000,
    ),
    beta: float = Query(
        default=0.01,
        ge=0.0,
    ),
    omega: int = Query(
        default=1000,
        ge=1,
    ),
    crawl_missing: bool = Query(default=False),
) -> Any:
    return run_full_aml_pipeline(
        address=address.strip(),
        max_depth=max_depth,
        max_addresses_per_layer=max_addresses_per_layer,
        beta=beta,
        omega=omega,
        crawl_missing=crawl_missing,
    )