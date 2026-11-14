#!/usr/bin/env python3
"""Negative tests for the isolated nutrient-evidence validator; no project data is modified."""
import copy
import json
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("nutrient_validator", ROOT / "validate-nutrient-evidence.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
SCHEMA = json.loads((ROOT / "nutrient-evidence.schema.json").read_text(encoding="utf-8"))
SAMPLE = json.loads((ROOT / "nutrient-evidence.sample.json").read_text(encoding="utf-8"))

def evidence(data=SAMPLE):
    return data["foods"][0]["nutrientEvidence"]["iron"][0]

class ValidatorNegativeTests(unittest.TestCase):
    def rejected(self, mutate, expected):
        data = copy.deepcopy(SAMPLE)
        mutate(data)
        with self.assertRaisesRegex(ValueError, expected):
            validator.validate(data, SCHEMA)

    def test_valid_research_only_sample_passes(self):
        self.assertEqual(validator.validate(copy.deepcopy(SAMPLE), SCHEMA), (1, 1, 1))

    def test_unknown_source_is_rejected(self):
        self.rejected(lambda d: evidence(d).__setitem__("sourceId", "MISSING-SOURCE"), "sourceId does not resolve")

    def test_duplicate_evidence_id_is_rejected(self):
        def mutate(d):
            duplicate = copy.deepcopy(evidence(d))
            d["foods"][0]["nutrientEvidence"]["iron"].append(duplicate)
        self.rejected(mutate, "Duplicate evidenceId")

    def test_approved_value_without_standard_value_is_rejected(self):
        def mutate(d):
            e = evidence(d); e["reviewStatus"] = "approved"; e["standardValue"] = None
            e["standardUnit"] = "mg/100g"; e["standardBasis"] = "edible portion"
        self.rejected(mutate, "approved evidence requires standardValue")

    def test_approved_value_without_unit_is_rejected(self):
        def mutate(d):
            e = evidence(d); e["reviewStatus"] = "approved"; e["standardValue"] = 3.76
            e["standardUnit"] = None; e["standardBasis"] = "edible portion"
        self.rejected(mutate, "approved evidence requires raw/standard basis and standard unit")

    def test_dry_weight_cannot_be_approved_as_edible_without_conversion(self):
        def mutate(d):
            e = evidence(d); e["reviewStatus"] = "approved"; e["standardValue"] = 3.76
            e["rawBasis"] = "per 100g dry matter"; e["standardBasis"] = "per 100g edible portion"
            e["standardUnit"] = "mg/100g"
        self.rejected(mutate, "dry-matter to edible-portion approval requires documented conversion")

    def test_dry_weight_conversion_requires_factor_and_inputs(self):
        def mutate(d):
            e = evidence(d); e["reviewStatus"] = "approved"; e["standardValue"] = 2.8
            e["rawBasis"] = "per 100g dry matter"; e["standardBasis"] = "per 100g edible portion"
            e["standardUnit"] = "mg/100g"
            e["conversion"] = {"formula": "dry_value * edible_dry_fraction", "factor": None, "inputs": {}, "note": "incomplete"}
        self.rejected(mutate, "dry-matter to edible-portion approval requires documented conversion")

    def test_research_only_is_not_implicitly_approved(self):
        self.assertEqual(evidence()["reviewStatus"], "research-only")
        self.assertIsNone(evidence()["standardValue"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
