from __future__ import annotations

import os
from pathlib import Path


# backend/app/config.py
APP_DIR = Path(__file__).resolve().parent

# D:\EthereumHeist_System\backend
BACKEND_DIR = APP_DIR.parent

# D:\EthereumHeist_System
DEFAULT_PROJECT_ROOT = BACKEND_DIR.parent


PROJECT_ROOT = Path(
    os.getenv(
        "PROJECT_BASE_DIR",
        str(DEFAULT_PROJECT_ROOT),
    )
).expanduser().resolve()


DATA_DIR = Path(
    os.getenv(
        "DATA_DIR",
        str(PROJECT_ROOT / "data"),
    )
).expanduser().resolve()


RESULTS_DIR = Path(
    os.getenv(
        "RESULTS_DIR",
        str(PROJECT_ROOT / "results"),
    )
).expanduser().resolve()


GRAPHS_DIR = Path(
    os.getenv(
        "GRAPHS_DIR",
        str(PROJECT_ROOT / "graphs"),
    )
).expanduser().resolve()


TRACKING_DIR = Path(
    os.getenv(
        "TRACKING_DIR",
        str(RESULTS_DIR / "tracking"),
    )
).expanduser().resolve()


EXPERIMENT_DIR = Path(
    os.getenv(
        "EXPERIMENT_DIR",
        str(RESULTS_DIR / "experiments"),
    )
).expanduser().resolve()


TRANSACTION_DIR = Path(
    os.getenv(
        "TRANSACTION_DIR",
        str(DATA_DIR / "transactions"),
    )
).expanduser().resolve()


def ensure_directories() -> None:
    """
    Create writable runtime directories when they do not exist.
    """
    directories = [
        DATA_DIR,
        RESULTS_DIR,
        GRAPHS_DIR,
        TRACKING_DIR,
        EXPERIMENT_DIR,
        TRANSACTION_DIR,
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )