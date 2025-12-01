import json
from pathlib import Path
import pandas as pd

# ---------------------------------------------------
# File paths (generic, no personal information)
# ---------------------------------------------------
INPUT_PATH = Path("input_data.json")

OUTPUT_INSTITUTIONS = Path("institutions.csv")
OUTPUT_AGENTS = Path("agents_with_parent.csv")

print("Input file:", INPUT_PATH.resolve())

if not INPUT_PATH.exists():
    raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")


# ---------------------------------------------------
# Load JSON
# ---------------------------------------------------
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Adjust index depending on JSON structure
entities_raw = data[1]


# ---------------------------------------------------
# Flattening function
# ---------------------------------------------------
def flatten_entity(entity):
    flattened = {
        "CA_OwnerID": entity.get("CA_OwnerID"),
        "EntityCode": entity.get("EntityCode"),
        "EntityType": entity.get("EntityType"),
        "EntityVersion": entity.get("__EBA_EntityVersion"),
    }

    # Extract general properties
    for prop in entity.get("Properties", []):
        for key, value in prop.items():
            if isinstance(value, list):
                flattened[key] = ", ".join(str(i) for i in value)
            else:
                flattened[key] = value

    # Extract services grouped by country
    service_entries = []
    for block in entity.get("Services", []):
        for country, services in block.items():
            if isinstance(services, list):
                for srv in services:
                    service_entries.append(f"{country}:{srv}")
            else:
                service_entries.append(f"{country}:{services}")
    flattened["Services"] = ", ".join(service_entries) if service_entries else None

    return flattened


# ---------------------------------------------------
# Create DataFrame
# ---------------------------------------------------
df_all = pd.DataFrame([flatten_entity(e) for e in entities_raw])

# Split by entity type
institutions = df_all[df_all["EntityType"] == "PSD_PI"].copy()
agents = df_all[df_all["EntityType"] == "PSD_AG"].copy()

# ---------------------------------------------------
# Parent entity mapping
# ---------------------------------------------------
parent_map = institutions[
    ["EntityCode", "ENT_NAM", "ENT_NAM_COM", "ENT_COU_RES"]
].rename(columns={
    "EntityCode": "Parent_EntityCode",
    "ENT_NAM": "Parent_Name",
    "ENT_NAM_COM": "Parent_Commercial_Name",
    "ENT_COU_RES": "Parent_Country"
})

# Join agents with their parent institutions
agents_joined = agents.merge(
    parent_map,
    how="left",
    left_on="ENT_COD_PAR_ENT",
    right_on="Parent_EntityCode"
)

# ---------------------------------------------------
# Save output CSV files (UTF-16 for Excel compatibility)
# ---------------------------------------------------
institutions.to_csv(OUTPUT_INSTITUTIONS, index=False, sep=";", encoding="utf-16")
agents_joined.to_csv(OUTPUT_AGENTS, index=False, sep=";", encoding="utf-16")

print("Done!")
print("Institutions CSV:", OUTPUT_INSTITUTIONS.resolve())
print("Agents (with parent) CSV:", OUTPUT_AGENTS.resolve())

