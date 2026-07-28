from pathlib import Path
import pandas as pd

BASE_DIR = Path(r"D:\EthereumHeist_System")
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def find_file(filename: str) -> Path:
    matches = list(RAW_DATA_DIR.rglob(filename))
    if not matches:
        raise FileNotFoundError(f"{filename} not found inside {RAW_DATA_DIR}")
    return matches[0]


def read_csv_safe(filename: str):
    file_path = find_file(filename)
    df = pd.read_csv(file_path)

    return {
        "file_name": filename,
        "file_path": str(file_path),
        "rows": int(len(df)),
        "columns": list(df.columns),
        "preview": df.head(10).fillna("").to_dict(orient="records"),
    }


def get_heist_events():
    return read_csv_safe("HeistEvent_Info - filtered.csv")


def get_heist_labels():
    return read_csv_safe("Heist label-etherscan.csv")


def get_service_provider_map():
    return read_csv_safe("Service_Provider_Map.csv")


def get_dataset_overview():
    files = [
        "Heist label-etherscan.csv",
        "HeistEvent_Info - filtered.csv",
        "HeistEvent_Info - origin.csv",
        "Service_Provider_Map.csv",
    ]

    overview = []

    for filename in files:
        try:
            file_path = find_file(filename)
            df = pd.read_csv(file_path)
            overview.append({
                "file_name": filename,
                "rows": int(len(df)),
                "columns": list(df.columns),
                "size_kb": round(file_path.stat().st_size / 1024, 2),
            })
        except Exception as e:
            overview.append({
                "file_name": filename,
                "error": str(e),
            })

    return {
        "dataset_root": str(RAW_DATA_DIR),
        "files": overview,
    }