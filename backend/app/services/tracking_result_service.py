from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


# =========================================================
# PROJECT PATHS
# =========================================================
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2]

BASE_DIR = Path(
    os.getenv(
        "PROJECT_BASE_DIR",
        str(BACKEND_DIR.parent),
    )
).resolve()

TRACKING_DIR = BASE_DIR / "results" / "tracking"

# =========================================================
# INTERNAL HELPERS
# =========================================================
def _get_safe_tracking_path(file_name: str) -> Path:
    """
    Return a safe absolute path inside the tracking directory.

    This prevents paths such as:
        ../../some_other_file.txt
    """

    if not file_name or not file_name.strip():
        raise ValueError("File name cannot be empty.")

    TRACKING_DIR.mkdir(parents=True, exist_ok=True)

    tracking_root = TRACKING_DIR.resolve()
    file_path = (TRACKING_DIR / file_name).resolve()

    try:
        file_path.relative_to(tracking_root)
    except ValueError as exc:
        raise ValueError(
            "Invalid file path. The file must be inside the tracking folder."
        ) from exc

    return file_path


def _file_not_found_response(file_name: str) -> dict[str, Any]:
    return {
        "success": False,
        "error": f"{file_name} not found",
        "tracking_folder": str(TRACKING_DIR),
    }


# =========================================================
# LIST TRACKING FILES
# =========================================================
def list_tracking_files() -> dict[str, Any]:
    """
    List all files available in:
        D:\\EthereumHeist_System\\results\\tracking
    """

    TRACKING_DIR.mkdir(parents=True, exist_ok=True)

    files: list[dict[str, Any]] = []

    for file_path in sorted(
        TRACKING_DIR.iterdir(),
        key=lambda item: item.name.lower(),
    ):
        if not file_path.is_file():
            continue

        stat = file_path.stat()

        files.append(
            {
                "file_name": file_path.name,
                "path": str(file_path),
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "extension": file_path.suffix.lower(),
                "modified_timestamp": stat.st_mtime,
            }
        )

    return {
        "success": True,
        "tracking_folder": str(TRACKING_DIR),
        "file_count": len(files),
        "files": files,
    }


# =========================================================
# PREVIEW TRACKING CSV
# =========================================================
def preview_tracking_file(
    file_name: str,
    preview_rows: int = 50,
) -> dict[str, Any]:
    """
    Preview a CSV tracking file.

    Parameters
    ----------
    file_name:
        Name of the CSV file located inside the tracking directory.

    preview_rows:
        Maximum number of rows returned in the preview.
    """

    try:
        file_path = _get_safe_tracking_path(file_name)
    except ValueError as exc:
        return {
            "success": False,
            "error": str(exc),
            "tracking_folder": str(TRACKING_DIR),
        }

    if not file_path.exists() or not file_path.is_file():
        return _file_not_found_response(file_name)

    if file_path.suffix.lower() != ".csv":
        return {
            "success": False,
            "error": (
                f"{file_name} is not a CSV file. "
                f"Detected extension: {file_path.suffix.lower() or 'none'}"
            ),
        }

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        return {
            "success": False,
            "error": f"{file_name} is empty or contains no readable columns.",
        }
    except pd.errors.ParserError as exc:
        return {
            "success": False,
            "error": f"Could not parse {file_name} as CSV.",
            "details": str(exc),
        }
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_path, encoding="latin-1")
        except Exception as exc:
            return {
                "success": False,
                "error": f"Could not decode {file_name}.",
                "details": str(exc),
            }
    except Exception as exc:
        return {
            "success": False,
            "error": f"Could not read {file_name}.",
            "details": str(exc),
        }

    preview_rows = max(1, min(int(preview_rows), 500))

    clean_preview = (
        df.head(preview_rows)
        .where(pd.notna(df.head(preview_rows)), "")
        .to_dict(orient="records")
    )

    return {
        "success": True,
        "file_name": file_name,
        "file_path": str(file_path),
        "rows": int(len(df)),
        "columns": [str(column) for column in df.columns],
        "column_count": int(len(df.columns)),
        "preview_row_count": len(clean_preview),
        "preview": clean_preview,
    }


def preview_tracking_csv(
    file_name: str,
    preview_rows: int = 50,
) -> dict[str, Any]:
    """
    Alias maintained for compatibility with existing imports in app.main.
    """

    return preview_tracking_file(
        file_name=file_name,
        preview_rows=preview_rows,
    )


# =========================================================
# READ TRACKING JSON SUMMARY
# =========================================================
def read_tracking_summary(file_name: str) -> dict[str, Any]:
    """
    Read a JSON summary file from the tracking directory.
    """

    try:
        file_path = _get_safe_tracking_path(file_name)
    except ValueError as exc:
        return {
            "success": False,
            "error": str(exc),
            "tracking_folder": str(TRACKING_DIR),
        }

    if not file_path.exists() or not file_path.is_file():
        return _file_not_found_response(file_name)

    if file_path.suffix.lower() != ".json":
        return {
            "success": False,
            "error": (
                f"{file_name} is not a JSON file. "
                f"Detected extension: {file_path.suffix.lower() or 'none'}"
            ),
        }

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as exc:
        return {
            "success": False,
            "error": f"{file_name} contains invalid JSON.",
            "details": str(exc),
        }

    except UnicodeDecodeError as exc:
        return {
            "success": False,
            "error": f"{file_name} could not be decoded as UTF-8.",
            "details": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": f"Could not open {file_name}.",
            "details": str(exc),
        }

    return {
        "success": True,
        "file_name": file_name,
        "file_path": str(file_path),
        "data": data,
    }