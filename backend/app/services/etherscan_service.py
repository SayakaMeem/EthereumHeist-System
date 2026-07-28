import os
import time
from pathlib import Path
from typing import Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(r"D:\EthereumHeist_System")
RAW_TX_DIR = BASE_DIR / "data" / "raw" / "transactions"
RAW_TX_DIR.mkdir(parents=True, exist_ok=True)

ETHERSCAN_API_URL = "https://api.etherscan.io/v2/api"
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
ETHERSCAN_CHAIN_ID = os.getenv("ETHERSCAN_CHAIN_ID", "1")


class EtherscanAPIError(Exception):
    pass


def _call_etherscan(action: str, address: str, page: int = 1, offset: int = 1000) -> List[Dict]:
    if not ETHERSCAN_API_KEY:
        raise EtherscanAPIError("ETHERSCAN_API_KEY is missing. Add it to backend/.env")

    params = {
        "chainid": ETHERSCAN_CHAIN_ID,
        "module": "account",
        "action": action,
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": page,
        "offset": offset,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY,
    }

    response = requests.get(ETHERSCAN_API_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if data.get("status") == "0" and data.get("message") == "No transactions found":
        return []

    if "result" not in data:
        raise EtherscanAPIError(f"Unexpected Etherscan response: {data}")

    if isinstance(data["result"], str):
        raise EtherscanAPIError(data["result"])

    return data["result"]


def fetch_address_transactions(address: str) -> Dict:
    address = address.strip()

    normal_txs = _call_etherscan("txlist", address)
    time.sleep(0.35)

    internal_txs = _call_etherscan("txlistinternal", address)
    time.sleep(0.35)

    erc20_txs = _call_etherscan("tokentx", address)
    time.sleep(0.35)

    normal_file = RAW_TX_DIR / f"{address}_normal.csv"
    internal_file = RAW_TX_DIR / f"{address}_internal.csv"
    erc20_file = RAW_TX_DIR / f"{address}_erc20.csv"

    pd.DataFrame(normal_txs).to_csv(normal_file, index=False)
    pd.DataFrame(internal_txs).to_csv(internal_file, index=False)
    pd.DataFrame(erc20_txs).to_csv(erc20_file, index=False)

    return {
        "address": address,
        "normal_transactions": len(normal_txs),
        "internal_transactions": len(internal_txs),
        "erc20_transactions": len(erc20_txs),
        "saved_files": {
            "normal": str(normal_file),
            "internal": str(internal_file),
            "erc20": str(erc20_file),
        },
    }