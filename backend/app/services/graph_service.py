from pathlib import Path
import pandas as pd

BASE_DIR = Path(r"D:\EthereumHeist_System")
TRACKING_DIR = BASE_DIR / "results" / "tracking"


def build_tracking_graph(file_name: str, limit: int = 30):
    file_path = TRACKING_DIR / file_name

    if not file_path.exists():
        return {
            "error": f"{file_name} not found",
            "tracking_folder": str(TRACKING_DIR),
        }

    df = pd.read_csv(file_path)

    if df.empty:
        return {
            "file_name": file_name,
            "nodes": [],
            "edges": [],
            "message": "No edge data found",
        }

    required_cols = {"source", "target"}
    if not required_cols.issubset(set(df.columns)):
        return {
            "error": "CSV must contain source and target columns",
            "columns": list(df.columns),
        }

    df = df.head(limit).copy()

    nodes_dict = {}
    edges = []

    for index, row in df.iterrows():
        source = str(row.get("source", "")).strip().lower()
        target = str(row.get("target", "")).strip().lower()

        if not source or not target:
            continue

        source_layer = int(row.get("source_layer", 0)) if "source_layer" in df.columns else 0
        target_layer = source_layer + 1

        label = str(row.get("label", "candidate_layering"))
        tx_type = str(row.get("transaction_type", "unknown"))
        amount = row.get("amount", "")

        if source not in nodes_dict:
            nodes_dict[source] = {
                "id": source,
                "label": source[:8] + "..." + source[-6:],
                "layer": source_layer,
                "role": "placement" if source_layer == 0 else "layering",
            }

        if target not in nodes_dict:
            nodes_dict[target] = {
                "id": target,
                "label": target[:8] + "..." + target[-6:],
                "layer": target_layer,
                "role": label,
            }

        edges.append({
            "id": f"edge-{index}",
            "source": source,
            "target": target,
            "transaction_type": tx_type,
            "amount": str(amount),
            "label": label,
        })

    return {
        "file_name": file_name,
        "limit": limit,
        "node_count": len(nodes_dict),
        "edge_count": len(edges),
        "nodes": list(nodes_dict.values()),
        "edges": edges,
    }