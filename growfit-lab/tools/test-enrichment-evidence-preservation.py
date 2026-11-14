#!/usr/bin/env python3
"""Regression tests: USDA enrichment must preserve inactive nutrient evidence."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("growfit_enrichment", ROOT / "enrich-food-bank.py")
enrichment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(enrichment)

SAMPLE = json.loads((ROOT / "nutrient-evidence.sample.json").read_text(encoding="utf-8"))
EVIDENCE = SAMPLE["foods"][0]["nutrientEvidence"]

class EnrichmentEvidencePreservationTests(unittest.TestCase):
    def setUp(self):
        self.food = {
            "id": 27,
            "name": "نان سنگک",
            "nutrientEvidence": copy.deepcopy(EVIDENCE),
            "micronutrientsPer100g": {"iron": None},
            "customResearchNote": {"keep": True},
        }
        self.evidence_before = copy.deepcopy(self.food["nutrientEvidence"])

    def test_usda_update_preserves_all_manual_evidence(self):
        micro = {key: None for key in enrichment.NUTRIENTS}
        micro["iron"] = 2.1
        enrichment.apply_usda_fields(
            self.food,
            {"status": "accepted", "fdcId": 123, "mappingMethod": "manual-reviewed"},
            micro,
        )
        self.assertEqual(self.food["nutrientEvidence"], self.evidence_before)
        self.assertEqual(self.food["micronutrientsPer100g"]["iron"], 2.1)
        self.assertEqual(self.food["customResearchNote"], {"keep": True})

    def test_repeated_usda_updates_do_not_duplicate_or_rewrite_evidence(self):
        for fdc_id in (123, 123):
            enrichment.apply_usda_fields(
                self.food,
                {"status": "accepted", "fdcId": fdc_id},
                {key: None for key in enrichment.NUTRIENTS},
            )
        self.assertEqual(self.food["nutrientEvidence"], self.evidence_before)
        self.assertEqual(len(self.food["nutrientEvidence"]["iron"]), 1)

    def test_food_without_evidence_stays_without_evidence(self):
        food = {"id": 1, "name": "test"}
        enrichment.apply_usda_fields(
            food, {"status": "accepted", "fdcId": 10},
            {key: None for key in enrichment.NUTRIENTS},
        )
        self.assertNotIn("nutrientEvidence", food)

    def test_research_only_value_never_enters_meal_aggregation(self):
        food = {
            "id": 27,
            "fdcMatch": {"status": "accepted", "fdcId": 123},
            "micronutrientsPer100g": {key: None for key in enrichment.NUTRIENTS},
            "nutrientEvidence": copy.deepcopy(EVIDENCE),
        }
        bank = {
            "foods": [food],
            "meals": [{
                "ingredients": [{"foodId": 0, "grams": 100}],
            }],
        }
        enrichment.aggregate_meals(bank)
        self.assertIsNone(bank["meals"][0]["micronutrients"]["iron"])
        self.assertEqual(bank["meals"][0]["micronutrientCoverage"]["status"], "pending")
        self.assertEqual(food["nutrientEvidence"], self.evidence_before)

if __name__ == "__main__":
    unittest.main(verbosity=2)
