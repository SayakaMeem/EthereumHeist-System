from pathlib import Path
import pandas as pd

BASE_DIR = Path(r"D:\EthereumHeist_System")
TX_DIR = BASE_DIR / "data" / "raw" / "transactions"


def list_transaction_files():
    TX_DIR.mkdir(parents=True, exist_ok=True)

    files = []
    for file in TX_DIR.glob("*.csv"):
        files.append({
            "file_name": file.name,
            "path": str(file),
            "size_kb": round(file.stat().st_size / 1024, 2),
        })

    return {
        "transaction_folder": str(TX_DIR),
        "file_count": len(files),
        "files": files,
    }


def preview_transaction_file(file_name: str):
    file_path = TX_DIR / file_name

    if not file_path.exists():
        return {
            "error": f"{file_name} not found",
            "transaction_folder": str(TX_DIR),
        }

    df = pd.read_csv(file_path)

    return {
        "file_name": file_name,
        "rows": int(len(df)),
        "columns": list(df.columns),
        "preview": df.head(10).fillna("").to_dict(orient="records"),
    }