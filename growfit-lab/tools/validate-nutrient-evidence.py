#!/usr/bin/env python3
"""Validate the inactive GrowFit nutrient-evidence prototype using Python stdlib only."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "nutrient-evidence.schema.json"
DATA_PATH = ROOT / "nutrient-evidence.sample.json"
NUTRIENTS = {
    "fiber", "calcium", "iron", "potassium", "magnesium", "zinc", "sodium",
    "phosphorus", "selenium", "copper",
    "vitaminA", "vitaminC", "vitaminD", "vitaminB12", "folate"
}
STATUSES = {"research-only", "needs-review", "approved", "rejected"}
DATA_TYPES = {"analytical", "calculated", "borrowed", "estimated"}
REQUIRED = {
    "evidenceId", "sourceId", "rawValue", "rawUnit", "rawBasis",
    "standardValue", "standardUnit", "standardBasis", "conversion",
    "foodState", "sampleCountry", "sampleRegion", "sampleYear",
    "sampleCount", "method", "dataType", "reviewStatus", "reviewNote"
}

def fail(message):
    raise ValueError(message)

def validate(data, schema):
    if not schema.get("$schema", "").endswith("2020-12/schema"):
        fail("Unexpected JSON Schema draft")
    if data.get("schemaVersion") != 1:
        fail("schemaVersion must be 1")
    sources, foods = data.get("sources"), data.get("foods")
    if not isinstance(sources, list) or not isinstance(foods, list):
        fail("sources and foods must be arrays")

    source_ids = [x.get("sourceId") for x in sources]
    if len(source_ids) != len(set(source_ids)):
        fail("Duplicate sourceId")
    for source in sources:
        for key in ("sourceId", "title", "sourceType"):
            if not source.get(key):
                fail(f"Source missing {key}")

    evidence_ids, food_ids = set(), set()
    for food in foods:
        food_id = food.get("foodId")
        if not isinstance(food_id, int) or isinstance(food_id, bool) or food_id < 0:
            fail("foodId must be a non-negative integer")
        if food_id in food_ids:
            fail(f"Duplicate foodId: {food_id}")
        food_ids.add(food_id)
        if not food.get("foodName"):
            fail(f"Food {food_id} has no foodName")
        evidence_map = food.get("nutrientEvidence")
        if not isinstance(evidence_map, dict):
            fail(f"Food {food_id}: nutrientEvidence must be an object")

        for nutrient, entries in evidence_map.items():
            if nutrient not in NUTRIENTS:
                fail(f"Food {food_id}: unsupported nutrient {nutrient}")
            if not isinstance(entries, list):
                fail(f"Food {food_id}/{nutrient}: evidence must be an array")
            for item in entries:
                if not isinstance(item, dict):
                    fail(f"{nutrient}: each evidence item must be an object")
                missing = REQUIRED - item.keys()
                if missing:
                    fail(f"{nutrient}: missing fields {sorted(missing)}")
                evidence_id = item["evidenceId"]
                if evidence_id in evidence_ids:
                    fail(f"Duplicate evidenceId: {evidence_id}")
                evidence_ids.add(evidence_id)
                if item["sourceId"] not in source_ids:
                    fail(f"{evidence_id}: sourceId does not resolve")
                if item["reviewStatus"] not in STATUSES:
                    fail(f"{evidence_id}: invalid reviewStatus")
                if item["dataType"] not in DATA_TYPES:
                    fail(f"{evidence_id}: invalid dataType")
                raw_value = item["rawValue"]
                if raw_value is not None and (not isinstance(raw_value, (int, float)) or isinstance(raw_value, bool)):
                    fail(f"{evidence_id}: rawValue must be numeric or null")
                if raw_value is not None and not item["rawUnit"]:
                    fail(f"{evidence_id}: rawValue requires rawUnit")
                if item["standardValue"] is not None and (
                    not isinstance(item["standardValue"], (int, float)) or isinstance(item["standardValue"], bool)
                ):
                    fail(f"{evidence_id}: standardValue must be numeric or null")

                conversion = item["conversion"]
                if conversion is not None:
                    if not isinstance(conversion, dict):
                        fail(f"{evidence_id}: conversion must be an object or null")
                    if not conversion.get("formula") or not isinstance(conversion.get("inputs"), dict):
                        fail(f"{evidence_id}: conversion requires formula and inputs object")

                if item["reviewStatus"] == "approved":
                    if item["standardValue"] is None:
                        fail(f"{evidence_id}: approved evidence requires standardValue")
                    if not item["standardUnit"] or not item["standardBasis"] or not item["rawBasis"]:
                        fail(f"{evidence_id}: approved evidence requires raw/standard basis and standard unit")
                    raw_basis = str(item["rawBasis"]).lower()
                    standard_basis = str(item["standardBasis"]).lower()
                    raw_is_dry = "dry" in raw_basis or "خشک" in raw_basis
                    standard_is_edible = "edible" in standard_basis or "خوراکی" in standard_basis
                    if raw_is_dry and standard_is_edible:
                        if not conversion or conversion.get("factor") is None or not conversion.get("inputs"):
                            fail(f"{evidence_id}: dry-matter to edible-portion approval requires documented conversion factor and inputs")

    return len(source_ids), len(foods), len(evidence_ids)

def main():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_PATH
    data = json.loads(data_path.read_text(encoding="utf-8"))
    sources, foods, evidence = validate(data, schema)
    print(f"PASS: {sources} source(s), {foods} food(s), {evidence} evidence record(s).")
    print("PASS: source links resolve; IDs are unique; review states and approval rules are valid.")
    print("NOTE: this validator does not write to the food bank or authorize meal calculations.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
