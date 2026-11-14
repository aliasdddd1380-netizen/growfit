#!/usr/bin/env python3
"""Controlled promotion of reviewed nutrient evidence into the lab food bank.

Default mode is a dry run. Use --apply only after independent scientific review.
Only one approved, normalized, source-backed value per food/nutrient can be published.
"""
import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
DEFAULT_BANK = ROOT / "growfit-lab/inbox/growfit-food-bank.json"
DEFAULT_EVIDENCE = TOOLS / "nutrient-evidence.sample.json"
SCHEMA_PATH = TOOLS / "nutrient-evidence.schema.json"
UNIT_BY_NUTRIENT = {
    "fiber": "g/100g",
    "calcium": "mg/100g",
    "iron": "mg/100g",
    "potassium": "mg/100g",
    "magnesium": "mg/100g",
    "zinc": "mg/100g",
    "sodium": "mg/100g",
    "vitaminA": "µg RAE/100g",
    "vitaminC": "mg/100g",
    "vitaminD": "µg/100g",
    "vitaminB12": "µg/100g",
    "folate": "µg/100g",
}
ALLOWED_BASIS = {"per 100g edible portion", "per 100 g edible portion", "edible portion per 100g"}
ALLOWED_SOURCE_TYPES = {"peer-reviewed-article", "government-database", "food-composition-table", "technical-report"}

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

validator = load_module("nutrient_validator", TOOLS / "validate-nutrient-evidence.py")
enrichment = load_module("growfit_enrichment", TOOLS / "enrich-food-bank.py")

def fail(message):
    raise ValueError(message)

def build_plan(package, bank):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator.validate(package, schema)
    source_map = {x["sourceId"]: x for x in package["sources"]}
    bank_foods = {x["id"]: x for x in bank.get("foods", [])}
    if len(bank_foods) != len(bank.get("foods", [])):
        fail("Food bank contains duplicate food IDs")

    candidates = {}
    rejected = []
    for food_record in package["foods"]:
        food_id = food_record["foodId"]
        target = bank_foods.get(food_id)
        if target is None:
            rejected.append({"foodId": food_id, "reason": "food-id-not-found"})
            continue
        if target.get("name") != food_record["foodName"]:
            rejected.append({"foodId": food_id, "reason": "food-name-mismatch"})
            continue
        for nutrient, entries in food_record["nutrientEvidence"].items():
            for evidence in entries:
                if evidence["reviewStatus"] != "approved":
                    continue
                reason = None
                source = source_map[evidence["sourceId"]]
                if evidence["dataType"] == "estimated":
                    reason = "estimated-data-not-publishable"
                elif source.get("sourceType") not in ALLOWED_SOURCE_TYPES:
                    reason = "source-type-not-eligible"
                elif not str(source.get("url") or "").startswith("https://"):
                    reason = "https-source-required"
                elif not evidence.get("method"):
                    reason = "method-required-for-publication"
                elif evidence.get("standardUnit") != UNIT_BY_NUTRIENT[nutrient]:
                    reason = "noncanonical-standard-unit"
                elif str(evidence.get("standardBasis") or "").strip().lower() not in ALLOWED_BASIS:
                    reason = "standard-basis-must-be-edible-portion-per-100g"
                elif evidence.get("standardValue") is None or not math.isfinite(float(evidence["standardValue"])) or float(evidence["standardValue"]) < 0:
                    reason = "invalid-standard-value"
                elif not evidence.get("rawUnit") or not evidence.get("rawBasis"):
                    reason = "raw-unit-and-basis-required"
                elif not evidence.get("foodState"):
                    reason = "food-state-required"
                else:
                    raw_basis = str(evidence["rawBasis"]).lower()
                    if ("dry" in raw_basis or "خشک" in raw_basis):
                        conversion = evidence.get("conversion") or {}
                        factor = conversion.get("factor")
                        if not isinstance(factor, (int, float)) or isinstance(factor, bool) or not math.isfinite(float(factor)) or factor <= 0 or not conversion.get("inputs"):
                            reason = "dry-matter-conversion-incomplete"
                if reason:
                    rejected.append({"foodId": food_id, "nutrient": nutrient, "evidenceId": evidence["evidenceId"], "reason": reason})
                    continue
                candidates.setdefault((food_id, nutrient), []).append((evidence, source))

    plan, conflicts = [], []
    for (food_id, nutrient), rows in sorted(candidates.items()):
        target = bank_foods[food_id]
        if len(rows) != 1:
            conflicts.append({"foodId": food_id, "nutrient": nutrient, "reason": "multiple-approved-evidence-records"})
            continue
        evidence, source = rows[0]
        current = (target.get("micronutrientsPer100g") or {}).get(nutrient)
        if current is not None:
            conflicts.append({"foodId": food_id, "nutrient": nutrient, "reason": "existing-value-not-overwritten", "existingValue": current})
            continue
        plan.append({
            "foodId": food_id,
            "foodName": target["name"],
            "nutrient": nutrient,
            "value": float(evidence["standardValue"]),
            "unit": UNIT_BY_NUTRIENT[nutrient],
            "evidence": evidence,
            "source": source,
        })
    return plan, rejected, conflicts

def apply_plan(bank, plan):
    food_map = {x["id"]: x for x in bank["foods"]}
    for item in plan:
        food = food_map[item["foodId"]]
        food.setdefault("micronutrientsPer100g", {})[item["nutrient"]] = item["value"]
        food.setdefault("micronutrientUnits", {})[item["nutrient"]] = item["unit"]
        food.setdefault("micronutrientProvenance", {})[item["nutrient"]] = {
            "evidenceId": item["evidence"]["evidenceId"],
            "sourceId": item["source"]["sourceId"],
            "sourceTitle": item["source"]["title"],
            "sourceUrl": item["source"]["url"],
            "sourceYear": item["source"].get("year"),
            "reviewStatus": "approved",
            "dataType": item["evidence"]["dataType"],
            "rawValue": item["evidence"]["rawValue"],
            "rawUnit": item["evidence"]["rawUnit"],
            "rawBasis": item["evidence"]["rawBasis"],
            "standardValue": item["value"],
            "standardUnit": item["unit"],
            "standardBasis": item["evidence"]["standardBasis"],
            "foodState": item["evidence"]["foodState"],
            "method": item["evidence"]["method"],
        }
    enrichment.aggregate_meals(bank)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", type=Path, default=DEFAULT_BANK)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--apply", action="store_true", help="write approved values to the lab bank; default is dry-run")
    args = parser.parse_args()
    bank = json.loads(args.bank.read_text(encoding="utf-8"))
    package = json.loads(args.evidence.read_text(encoding="utf-8"))
    plan, rejected, conflicts = build_plan(package, bank)
    print(f"Eligible approved values: {len(plan)}")
    print(f"Skipped/rejected records: {len(rejected)}")
    print(f"Conflicts requiring review: {len(conflicts)}")
    for row in rejected + conflicts:
        print("REVIEW " + json.dumps(row, ensure_ascii=False, sort_keys=True))
    for row in plan:
        print("READY " + json.dumps({k: row[k] for k in ("foodId", "foodName", "nutrient", "value", "unit")}, ensure_ascii=False))
    if not args.apply:
        print("DRY RUN: no files changed. Re-run with --apply only after scientific review.")
        return 0
    if rejected or conflicts:
        print("REFUSING --apply: resolve all rejected records and conflicts first.", file=sys.stderr)
        return 2
    if plan:
        apply_plan(bank, plan)
        args.bank.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"APPLIED: {len(plan)} approved nutrient value(s).")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
