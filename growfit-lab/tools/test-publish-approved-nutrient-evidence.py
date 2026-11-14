#!/usr/bin/env python3
"""Tests for the gated evidence publisher and approved-provenance aggregation."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("evidence_publisher", ROOT / "publish-approved-nutrient-evidence.py")
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)
SAMPLE = json.loads((ROOT / "nutrient-evidence.sample.json").read_text(encoding="utf-8"))

def package_with_approved_value():
    package = copy.deepcopy(SAMPLE)
    e = package["foods"][0]["nutrientEvidence"]["iron"][0]
    e.update({
        "rawValue": 2.5,
        "rawUnit": "mg/100g",
        "rawBasis": "per 100g fresh edible portion",
        "standardValue": 2.5,
        "standardUnit": "mg/100g",
        "standardBasis": "per 100g edible portion",
        "foodState": "baked",
        "method": "ICP-MS",
        "reviewStatus": "approved",
        "reviewNote": "Reviewed example fixture",
    })
    return package

def bank_fixture(existing_iron=None):
    micro = {key: None for key in publisher.enrichment.NUTRIENTS}
    micro["iron"] = existing_iron
    foods = [{
        "id": index,
        "name": f"fixture-{index}",
        "micronutrientsPer100g": {key: None for key in publisher.enrichment.NUTRIENTS},
        "fdcMatch": {"status": "review"},
    } for index in range(27)]
    foods.append({
        "id": 27,
        "name": "نان سنگک",
        "micronutrientsPer100g": micro,
        "micronutrientUnits": {key: value[2] for key, value in publisher.enrichment.NUTRIENTS.items()},
        "fdcMatch": {"status": "review"},
    })
    return {
        "foods": foods,
        "meals": [{
            "id": 1,
            "ingredients": [{"foodId": 27, "grams": 100}],
        }],
    }

class ApprovedEvidencePublisherTests(unittest.TestCase):
    def test_research_only_sample_is_never_publishable(self):
        plan, rejected, conflicts = publisher.build_plan(copy.deepcopy(SAMPLE), bank_fixture())
        self.assertEqual(plan, [])
        self.assertEqual(rejected, [])
        self.assertEqual(conflicts, [])

    def test_approved_value_is_published_with_full_provenance_and_aggregated(self):
        package = package_with_approved_value()
        bank = bank_fixture()
        plan, rejected, conflicts = publisher.build_plan(package, bank)
        self.assertEqual(len(plan), 1)
        self.assertEqual(rejected, [])
        self.assertEqual(conflicts, [])
        publisher.apply_plan(bank, plan)
        food = bank["foods"][0]
        self.assertEqual(food["micronutrientsPer100g"]["iron"], 2.5)
        self.assertEqual(food["micronutrientProvenance"]["iron"]["evidenceId"], "SANGAK-IRON-2012-A")
        self.assertEqual(bank["meals"][0]["micronutrients"]["iron"], 2.5)
        self.assertEqual(bank["meals"][0]["micronutrientSources"][0]["sourceId"], "SANGAK-BARBARI-MINERALS-2012")

    def test_multiple_approved_records_for_same_nutrient_are_blocked(self):
        package = package_with_approved_value()
        duplicate = copy.deepcopy(package["foods"][0]["nutrientEvidence"]["iron"][0])
        duplicate["evidenceId"] = "SANGAK-IRON-SECOND"
        package["foods"][0]["nutrientEvidence"]["iron"].append(duplicate)
        plan, rejected, conflicts = publisher.build_plan(package, bank_fixture())
        self.assertEqual(plan, [])
        self.assertEqual(conflicts[0]["reason"], "multiple-approved-evidence-records")

    def test_existing_usda_value_is_never_overwritten(self):
        plan, rejected, conflicts = publisher.build_plan(package_with_approved_value(), bank_fixture(existing_iron=1.8))
        self.assertEqual(plan, [])
        self.assertEqual(conflicts[0]["reason"], "existing-value-not-overwritten")

    def test_reapplying_same_approved_evidence_is_idempotent(self):
        bank = bank_fixture()
        package = package_with_approved_value()
        plan, _, _ = publisher.build_plan(package, bank)
        publisher.apply_plan(bank, plan)
        second_plan, rejected, conflicts = publisher.build_plan(package, bank)
        self.assertEqual(second_plan, [])
        self.assertEqual(rejected, [])
        self.assertEqual(conflicts, [])

    def test_wrong_unit_is_rejected(self):
        package = package_with_approved_value()
        package["foods"][0]["nutrientEvidence"]["iron"][0]["standardUnit"] = "µg/100g"
        plan, rejected, conflicts = publisher.build_plan(package, bank_fixture())
        self.assertEqual(plan, [])
        self.assertEqual(rejected[0]["reason"], "noncanonical-standard-unit")

    def test_estimated_data_is_rejected(self):
        package = package_with_approved_value()
        package["foods"][0]["nutrientEvidence"]["iron"][0]["dataType"] = "estimated"
        plan, rejected, conflicts = publisher.build_plan(package, bank_fixture())
        self.assertEqual(plan, [])
        self.assertEqual(rejected[0]["reason"], "estimated-data-not-publishable")

    def test_non_https_source_is_rejected(self):
        package = package_with_approved_value()
        package["sources"][0]["url"] = "http://example.org/paper"
        plan, rejected, conflicts = publisher.build_plan(package, bank_fixture())
        self.assertEqual(plan, [])
        self.assertEqual(rejected[0]["reason"], "https-source-required")

    def test_missing_method_is_rejected(self):
        package = package_with_approved_value()
        package["foods"][0]["nutrientEvidence"]["iron"][0]["method"] = None
        plan, rejected, conflicts = publisher.build_plan(package, bank_fixture())
        self.assertEqual(plan, [])
        self.assertEqual(rejected[0]["reason"], "method-required-for-publication")

    def test_insufficient_review_note_is_rejected(self):
        package = package_with_approved_value()
        package["foods"][0]["nutrientEvidence"]["iron"][0]["reviewNote"] = "ok"
        plan, rejected, conflicts = publisher.build_plan(package, bank_fixture())
        self.assertEqual(plan, [])
        self.assertEqual(rejected[0]["reason"], "substantive-review-note-required")

    def test_negative_raw_value_is_rejected(self):
        package = package_with_approved_value()
        package["foods"][0]["nutrientEvidence"]["iron"][0]["rawValue"] = -1
        plan, rejected, conflicts = publisher.build_plan(package, bank_fixture())
        self.assertEqual(plan, [])
        self.assertEqual(rejected[0]["reason"], "invalid-raw-value")

    def test_documented_dry_matter_conversion_can_pass(self):
        package = package_with_approved_value()
        e = package["foods"][0]["nutrientEvidence"]["iron"][0]
        e["rawBasis"] = "per 100g dry matter"
        e["conversion"] = {
            "formula": "dry_matter_value * edible_dry_fraction",
            "factor": 0.75,
            "inputs": {"edible_dry_fraction": 0.75},
            "note": "Measured moisture basis and documented conversion",
        }
        plan, rejected, conflicts = publisher.build_plan(package, bank_fixture())
        self.assertEqual(len(plan), 1)
        self.assertEqual(rejected, [])
        self.assertEqual(conflicts, [])

    def test_food_name_mismatch_is_rejected(self):
        package = package_with_approved_value()
        package["foods"][0]["foodName"] = "نام نادرست"
        plan, rejected, conflicts = publisher.build_plan(package, bank_fixture())
        self.assertEqual(plan, [])
        self.assertEqual(rejected[0]["reason"], "food-name-mismatch")

    def test_dry_matter_without_documented_conversion_is_rejected(self):
        package = package_with_approved_value()
        e = package["foods"][0]["nutrientEvidence"]["iron"][0]
        e["rawBasis"] = "per 100g dry matter"
        with self.assertRaisesRegex(ValueError, "dry-matter to edible-portion approval requires documented conversion"):
            publisher.build_plan(package, bank_fixture())

    def test_usda_refresh_preserves_approved_alternative_value_when_missing(self):
        bank = bank_fixture()
        plan, _, _ = publisher.build_plan(package_with_approved_value(), bank)
        publisher.apply_plan(bank, plan)
        food = bank["foods"][0]
        before = copy.deepcopy(food["micronutrientProvenance"])
        empty_micro = {key: None for key in publisher.enrichment.NUTRIENTS}
        publisher.enrichment.apply_usda_fields(food, {"status": "accepted", "fdcId": 123}, empty_micro)
        self.assertEqual(food["micronutrientsPer100g"]["iron"], 2.5)
        self.assertEqual(food["micronutrientProvenance"], before)

    def test_usda_non_null_value_takes_precedence_and_clears_old_provenance(self):
        bank = bank_fixture()
        plan, _, _ = publisher.build_plan(package_with_approved_value(), bank)
        publisher.apply_plan(bank, plan)
        food = bank["foods"][0]
        micro = {key: None for key in publisher.enrichment.NUTRIENTS}
        micro["iron"] = 1.9
        publisher.enrichment.apply_usda_fields(food, {"status": "accepted", "fdcId": 123}, micro)
        self.assertEqual(food["micronutrientsPer100g"]["iron"], 1.9)
        self.assertNotIn("iron", food.get("micronutrientProvenance", {}))

if __name__ == "__main__":
    unittest.main(verbosity=2)
