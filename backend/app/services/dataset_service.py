from pathlib import Path

BASE_DIR = Path(r"D:\EthereumHeist_System")
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
PARQUET_DATA_DIR = BASE_DIR / "data" / "parquet"


def get_dataset_status():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PARQUET_DATA_DIR.mkdir(parents=True, exist_ok=True)

    raw_files = []
    for file in RAW_DATA_DIR.rglob("*"):
        if file.is_file():
            raw_files.append({
                "name": file.name,
                "path": str(file),
                "size_mb": round(file.stat().st_size / (1024 * 1024), 3),
                "extension": file.suffix.lower()
            })

    return {
        "raw_data_path": str(RAW_DATA_DIR),
        "processed_data_path": str(PROCESSED_DATA_DIR),
        "parquet_data_path": str(PARQUET_DATA_DIR),
        "raw_file_count": len(raw_files),
        "raw_files": raw_files
    }