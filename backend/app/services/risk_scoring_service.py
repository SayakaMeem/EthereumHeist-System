from pathlib import Path
import pandas as pd

BASE_DIR = Path(r"D:\EthereumHeist_System")
TRACKING_DIR = BASE_DIR / "results" / "tracking"


def _to_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def _risk_level(score: int):
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 35:
        return "Medium"
    return "Low"


def add_risk_scores_to_edges(edges_file_name: str):
    safe_file_name = Path(edges_file_name).name
    edges_path = TRACKING_DIR / safe_file_name

    if not edges_path.exists():
        return {
            "error": f"{safe_file_name} not found",
            "tracking_folder": str(TRACKING_DIR),
        }

    df = pd.read_csv(edges_path, dtype=str).fillna("")

    required_cols = ["source", "target", "transaction_type", "amount"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        return {
            "error": "Required columns missing",
            "missing_columns": missing,
            "available_columns": list(df.columns),
        }

    risk_scores = []
    risk_reasons = []

    for _, row in df.iterrows():
        score = 0
        reasons = []

        amount = _to_float(row.get("amount", 0))
        transaction_type = str(row.get("transaction_type", "")).lower()
        label = str(row.get("label", "")).lower()
        token_symbol = str(row.get("tokenSymbol", "")).upper()
        target = str(row.get("target", "")).lower()

        if amount >= 1000000:
            score += 30
            reasons.append("very_large_amount")
        elif amount >= 100000:
            score += 20
            reasons.append("large_amount")
        elif amount >= 10000:
            score += 10
            reasons.append("medium_large_amount")

        if transaction_type == "erc20":
            score += 15
            reasons.append("erc20_token_transfer")

        if transaction_type == "normal_eth":
            score += 10
            reasons.append("normal_eth_transfer")

        if label == "candidate_layering":
            score += 20
            reasons.append("candidate_layering_address")

        if token_symbol in ["USDT", "USDC", "DAI"]:
            score += 15
            reasons.append("stablecoin_transfer")

        if target == "0x0000000000000000000000000000000000000000":
            score += 10
            reasons.append("zero_or_burn_address")

        if str(row.get("is_service_provider", "")).lower() == "true":
            score += 30
            reasons.append("matched_service_provider")

        if str(row.get("service_provider_category", "")).strip():
            category = str(row.get("service_provider_category", "")).lower()

            if "mixer" in category:
                score += 40
                reasons.append("mixer_interaction")
            elif "exchange" in category:
                score += 30
                reasons.append("exchange_interaction")
            elif "bridge" in category:
                score += 25
                reasons.append("bridge_interaction")
            elif "dex" in category:
                score += 20
                reasons.append("dex_interaction")

        if score > 100:
            score = 100

        risk_scores.append(score)
        risk_reasons.append(", ".join(reasons))

    df["risk_score"] = risk_scores
    df["risk_level"] = [_risk_level(score) for score in risk_scores]
    df["risk_reasons"] = risk_reasons

    output_file = TRACKING_DIR / f"{Path(safe_file_name).stem}_risk_scored.csv"
    df.to_csv(output_file, index=False)

    summary = {
        "Low": int((df["risk_level"] == "Low").sum()),
        "Medium": int((df["risk_level"] == "Medium").sum()),
        "High": int((df["risk_level"] == "High").sum()),
        "Critical": int((df["risk_level"] == "Critical").sum()),
    }

    return {
        "input_file": str(edges_path),
        "output_file": str(output_file),
        "total_edges": int(len(df)),
        "risk_summary": summary,
        "average_risk_score": float(df["risk_score"].mean()) if len(df) else 0,
        "max_risk_score": int(df["risk_score"].max()) if len(df) else 0,
        "preview": df.head(20).fillna("").to_dict(orient="records"),
    }