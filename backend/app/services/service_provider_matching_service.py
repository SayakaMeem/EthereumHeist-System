from pathlib import Path
import re
import pandas as pd

BASE_DIR = Path(r"D:\EthereumHeist_System")
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
TRACKING_DIR = BASE_DIR / "results" / "tracking"

# Force backend to use this exact service-provider file
SERVICE_PROVIDER_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "EthereumHeist-main"
    / "Service_Provider_Map.csv"
)


def _normalize_address(value):
    if pd.isna(value):
        return ""

    text = str(value).strip().lower()
    text = text.replace('"', "").replace("'", "")

    match = re.search(r"0x[a-f0-9]{40}", text)

    if match:
        return match.group(0)

    return ""


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(col).strip().replace("\ufeff", "") for col in df.columns]
    return df


def _find_address_columns(df: pd.DataFrame):
    address_columns = []

    for col in df.columns:
        col_lower = str(col).strip().lower()

        if (
            col_lower == "address"
            or "address" in col_lower
            or "account" in col_lower
            or "wallet" in col_lower
            or "addr" in col_lower
        ):
            address_columns.append(col)

    # Extra fallback: detect columns that contain Ethereum addresses
    for col in df.columns:
        if col in address_columns:
            continue

        sample_values = df[col].dropna().astype(str).head(100)

        for value in sample_values:
            if _normalize_address(value):
                address_columns.append(col)
                break

    return address_columns


def _pick_first_existing(row, possible_columns):
    for col in possible_columns:
        if col in row.index:
            value = str(row[col]).strip()
            if value and value.lower() not in ["nan", "none", "null", ""]:
                return value

    return ""


def _build_service_provider_lookup(service_df: pd.DataFrame):
    service_df = _clean_columns(service_df)
    address_columns = _find_address_columns(service_df)

    service_lookup = {}

    for _, row in service_df.iterrows():
        for col in address_columns:
            address = _normalize_address(row[col])

            if not address:
                continue

            service_name = _pick_first_existing(
                row,
                [
                    "name",
                    "Name",
                    "service",
                    "Service",
                    "provider",
                    "Provider",
                    "label",
                    "Label",
                    "entity",
                    "Entity",
                    "tag",
                    "Tag",
                    "Service Provider Name",
                ],
            )

            service_category = _pick_first_existing(
                row,
                [
                    "category",
                    "Category",
                    "type",
                    "Type",
                    "class",
                    "Class",
                    "service_type",
                    "Service Type",
                ],
            )

            service_source = _pick_first_existing(
                row,
                [
                    "source",
                    "Source",
                ],
            )

            service_note = _pick_first_existing(
                row,
                [
                    "note",
                    "Note",
                    "notes",
                    "Notes",
                ],
            )

            if not service_name:
                service_name = "Known Service Provider"

            if not service_category:
                service_category = "Unknown Service Type"

            service_lookup[address] = {
                "service_provider_name": service_name,
                "service_provider_category": service_category,
                "service_provider_source": service_source,
                "service_provider_note": service_note,
            }

    return service_lookup, address_columns


def enrich_edges_with_service_providers(edges_file_name: str):
    safe_file_name = Path(edges_file_name).name
    edges_path = TRACKING_DIR / safe_file_name

    if not edges_path.exists():
        return {
            "error": f"{safe_file_name} not found",
            "tracking_folder": str(TRACKING_DIR),
        }

    service_path = SERVICE_PROVIDER_FILE

    if not service_path.exists():
        return {
            "error": "Service_Provider_Map.csv not found in exact expected folder",
            "expected_service_provider_file": str(service_path),
        }

    edges_df = pd.read_csv(edges_path, dtype=str)
    service_df = pd.read_csv(service_path, dtype=str)

    edges_df = _clean_columns(edges_df)
    service_df = _clean_columns(service_df)

    service_lookup, detected_address_columns = _build_service_provider_lookup(service_df)

    if "source" not in edges_df.columns or "target" not in edges_df.columns:
        return {
            "error": "Edges file must contain source and target columns.",
            "edges_file": str(edges_path),
            "available_columns": list(edges_df.columns),
        }

    edges_df["source_clean"] = edges_df["source"].apply(_normalize_address)
    edges_df["target_clean"] = edges_df["target"].apply(_normalize_address)

    service_names = []
    service_categories = []
    service_sources = []
    service_notes = []
    matched_sides = []
    is_service_provider_values = []

    for _, row in edges_df.iterrows():
        source_address = row["source_clean"]
        target_address = row["target_clean"]

        target_match = service_lookup.get(target_address)
        source_match = service_lookup.get(source_address)

        # Main matching: target address is known service/downstream mapped address
        if target_match:
            service_names.append(target_match["service_provider_name"])
            service_categories.append(target_match["service_provider_category"])
            service_sources.append(target_match["service_provider_source"])
            service_notes.append(target_match["service_provider_note"])
            matched_sides.append("target")
            is_service_provider_values.append(True)

        # Secondary information: source address is found in service map
        elif source_match:
            service_names.append(source_match["service_provider_name"])
            service_categories.append(source_match["service_provider_category"])
            service_sources.append(source_match["service_provider_source"])
            service_notes.append(source_match["service_provider_note"])
            matched_sides.append("source")
            is_service_provider_values.append(False)

        else:
            service_names.append("")
            service_categories.append("")
            service_sources.append("")
            service_notes.append("")
            matched_sides.append("none")
            is_service_provider_values.append(False)

    edges_df["is_service_provider"] = is_service_provider_values
    edges_df["service_matched_side"] = matched_sides
    edges_df["service_provider_name"] = service_names
    edges_df["service_provider_category"] = service_categories
    edges_df["service_provider_source"] = service_sources
    edges_df["service_provider_note"] = service_notes

    output_file = TRACKING_DIR / f"{Path(safe_file_name).stem}_service_enriched.csv"
    edges_df.to_csv(output_file, index=False)

    matched_df = edges_df[edges_df["is_service_provider"] == True]
    unmatched_df = edges_df[edges_df["is_service_provider"] == False]

    matched_service_provider_edges = int(len(matched_df))

    if matched_service_provider_edges > 0:
        unique_service_providers = int(matched_df["target_clean"].nunique())
    else:
        unique_service_providers = 0

    edge_targets = set(edges_df["target_clean"].dropna().tolist())
    service_addresses = set(service_lookup.keys())
    overlap_addresses = sorted(list(edge_targets.intersection(service_addresses)))

    return {
        "edges_file": str(edges_path),
        "service_provider_file": str(service_path),
        "detected_service_address_columns": [str(col) for col in detected_address_columns],
        "service_provider_csv_rows": int(len(service_df)),
        "known_service_provider_addresses": int(len(service_lookup)),
        "unique_edge_target_addresses": int(len(edge_targets)),
        "overlap_address_count": int(len(overlap_addresses)),
        "overlap_addresses_preview": overlap_addresses[:20],
        "total_edges": int(len(edges_df)),
        "matched_service_provider_edges": matched_service_provider_edges,
        "unmatched_edges": int(len(unmatched_df)),
        "unique_service_providers": unique_service_providers,
        "output_file": str(output_file),
        "matched_preview": matched_df.head(20).fillna("").to_dict(orient="records"),
        "unmatched_preview": unmatched_df.head(10).fillna("").to_dict(orient="records"),
    }