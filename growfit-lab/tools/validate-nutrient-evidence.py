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
    "vitaminA", "vitaminC", "vitaminD", "vitaminB12", "folate"
}
STATUSES = {"research-only", "needs-review", "approved", "rejected"}
DATA_TYPES = {"analytical", "calculated", "borrowed", "estimated"}

def fail(message):
    raise ValueError(message)

def main():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    assert schema.get("$schema", "").endswith("2020-12/schema"), "Unexpected JSON Schema draft"
    assert data.get("schemaVersion") == 1, "schemaVersion must be 1"

    sources = data.get("sources")
    foods = data.get("foods")
    if not isinstance(sources, list) or not isinstance(foods, list):
        fail("sources and foods must be arrays")

    source_ids = [x.get("sourceId") for x in sources]
    if len(source_ids) != len(set(source_ids)):
        fail("Duplicate sourceId")
    evidence_ids = []
    food_ids = set()

    for source in sources:
        for key in ("sourceId", "title", "sourceType"):
            if not source.get(key):
                fail(f"Source missing {key}")

    for food in foods:
        food_id = food.get("foodId")
        if not isinstance(food_id, int) or food_id < 0:
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
                required = {
                    "evidenceId", "sourceId", "rawValue", "rawUnit", "rawBasis",
                    "standardValue", "standardUnit", "standardBasis", "conversion",
                    "foodState", "sampleCountry", "sampleRegion", "sampleYear",
                    "sampleCount", "method", "dataType", "reviewStatus", "reviewNote"
                }
                missing = required - item.keys()
                if missing:
                    fail(f"{nutrient}: missing fields {sorted(missing)}")
                evidence_id = item["evidenceId"]
                if evidence_id in evidence_ids:
                    fail(f"Duplicate evidenceId: {evidence_id}")
                evidence_ids.append(evidence_id)
                if item["sourceId"] not in source_ids:
                    fail(f"{evidence_id}: sourceId does not resolve")
                if item["reviewStatus"] not in STATUSES:
                    fail(f"{evidence_id}: invalid reviewStatus")
                if item["dataType"] not in DATA_TYPES:
                    fail(f"{evidence_id}: invalid dataType")
                if item["rawValue"] is not None and not isinstance(item["rawValue"], (int, float)):
                    fail(f"{evidence_id}: rawValue must be numeric or null")
                if item["rawValue"] is not None and not item["rawUnit"]:
                    fail(f"{evidence_id}: rawValue requires rawUnit")
                if item["reviewStatus"] == "approved":
                    if item["standardValue"] is None:
                        fail(f"{evidence_id}: approved evidence requires standardValue")
                    if not item["standardUnit"] or not item["standardBasis"]:
                        fail(f"{evidence_id}: approved evidence requires standard unit and basis")
                    if not item["rawBasis"]:
                        fail(f"{evidence_id}: approved evidence requires raw basis")
                if item["standardValue"] is None and item["reviewStatus"] == "approved":
                    fail(f"{evidence_id}: null cannot be approved")
                if item["conversion"] is not None and not isinstance(item["conversion"], dict):
                    fail(f"{evidence_id}: conversion must be an object or null")

    print(f"PASS: {len(sources)} source(s), {len(foods)} food(s), {len(evidence_ids)} evidence record(s).")
    print("PASS: all source links resolve; evidence IDs are unique; inactive/review statuses are valid.")
    print("NOTE: this validator does not write to the food bank or authorize meal calculations.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
