# GrowFit Lab — USDA food composition enrichment

This tool enriches the extracted GrowFit food bank with fiber, vitamins, and minerals using USDA FoodData Central.

## Security

- Never place an API key in source code, JSON files, HTML, or commits.
- The workflow reads the key only from the GitHub Actions secret named `USDA_API_KEY`.
- If the secret is absent, the script exits safely and leaves nutrient values unknown (not zero).

## One-time setup

1. Obtain a FoodData Central API key from the official USDA FoodData Central developer/API documentation.
2. In the GrowFit GitHub repository, open **Settings → Secrets and variables → Actions**.
3. Create a repository secret named exactly `USDA_API_KEY` and paste the key into its secret value.
4. Open **Actions → Publish GrowFit Lab Preview → Run workflow**. If manual dispatch is unavailable, a lab-only commit under `growfit-lab/tools/` or `growfit-lab/inbox/` also starts the workflow. The workflow never requires the key to be committed.

## Matching and data quality

- The search terms in `food-search-terms.json` cover all 113 source food records.
- The script searches Foundation Foods, SR Legacy, and FNDDS, then fetches the selected food's full nutrient profile.
- Only strong name/preparation matches are accepted automatically. Ambiguous records are written to `growfit-food-bank-review.json` for review.
- Missing nutrient values remain `null`; they are never treated as zero.
- Meal totals are calculated from ingredient weights. A nutrient total remains unknown if one or more ingredients lack that nutrient value.
- Persian breads, regional products, and branded items may require manual review or a local verified composition record.

## Files

- `enrich-food-bank.py`: enrichment and aggregation pipeline.
- `food-search-terms.json`: English search descriptions for the 113 food records.
- Output: `../inbox/growfit-food-bank.json` and `../inbox/growfit-food-bank-review.json`.

Source: USDA FoodData Central. Cite USDA FoodData Central in the application when displaying nutrient information.

## Nutrient evidence prototype (inactive)

The nutrient-level provenance prototype is deliberately isolated from the live food bank and nutrition UI.

Files:
- `nutrient-evidence.schema.json`: JSON Schema (Draft 2020-12) for source catalogues, foods, and per-nutrient evidence.
- `nutrient-evidence.sample.json`: one research-only Sangak iron example; the reported value is preserved but its normalized value remains null because the moisture/portion basis is unresolved.
- `validate-nutrient-evidence.py`: dependency-free Python validator for IDs, source references, nutrient names, review states, and approval requirements.
- `publish-approved-nutrient-evidence.py`: gated promotion tool; dry-run by default, requires `--apply` to write and refuses unresolved records/conflicts.
- `test-publish-approved-nutrient-evidence.py`: promotion, provenance, aggregation, collision, and USDA precedence regression tests.

Run locally from this directory:

```bash
python validate-nutrient-evidence.py
```

The provenance package remains **inactive**: it is not a source for meal totals and is not read by the nutrition page. The USDA enrichment pipeline has a narrow preservation guard: when it updates USDA-owned fields (`fdcMatch`, `micronutrientsPer100g`, and units), it verifies that any existing `nutrientEvidence` object remains byte-for-byte equivalent as parsed JSON. Meal aggregation continues to read only the approved legacy `micronutrientsPer100g` fields and never derives values from research evidence.

### Validation and regression tests

Run the full local check from this directory:

```bash
python -m py_compile enrich-food-bank.py validate-nutrient-evidence.py publish-approved-nutrient-evidence.py test-nutrient-evidence-validator.py test-enrichment-evidence-preservation.py test-publish-approved-nutrient-evidence.py
python validate-nutrient-evidence.py
python test-nutrient-evidence-validator.py
python test-enrichment-evidence-preservation.py
python test-publish-approved-nutrient-evidence.py
python publish-approved-nutrient-evidence.py
```

The validator suite covers valid research-only data, unresolved source IDs, duplicate evidence IDs, incomplete approvals, and missing dry-matter conversion evidence. The enrichment regression suite covers preservation across USDA updates, repeated updates, foods without evidence, and the rule that research-only and needs-review values do not enter meal aggregation. The promotion suite covers research-only exclusion, approved-value publication, source attribution, meal aggregation, duplicate approvals, existing-value conflicts, unit/basis restrictions, estimated-data rejection, food identity, dry-matter conversion, and USDA precedence. Tests use in-memory fixtures and do not write to the food bank.

The GitHub Pages workflow runs these checks. It also detects whether a push changed files under `growfit-lab/inbox/`; USDA enrichment and the bot commit are skipped for tools-only changes. This prevents editing documentation, schemas, or tests from unexpectedly rewriting the food bank. A manual workflow dispatch still explicitly runs the enrichment step.

### Activation boundary

- No evidence has been copied into `micronutrientsPer100g`.
- No meal total is calculated from `nutrientEvidence`.
- No food-bank nutrient value has been published from research evidence; the nutrition page was updated only to show source attribution if approved alternative values are present.
- Phase 2 now has a gated publisher and tests. The default command is dry-run; writing requires an explicit `--apply`, and the tool refuses unresolved records, multiple approvals, and overwriting an existing nutrient value. No current sample value is approved, so the dry-run should publish zero values.


### Controlled publication

The publisher accepts only approved, source-backed, non-estimated records with canonical units, a per-100g edible-portion basis, raw basis/unit, food state, and analytical method. It verifies the source URL, food ID/name, and dry-matter conversion metadata. It refuses to overwrite any existing nutrient value; conflicts must be reviewed outside the tool. Published values retain their source/evidence metadata in `micronutrientProvenance`, and meal totals include only values with an accepted USDA match or an approved provenance record.

Run a dry-run first:

```bash
python publish-approved-nutrient-evidence.py
```

Only after a separate scientific review, explicitly publish:

```bash
python publish-approved-nutrient-evidence.py --apply
```

The GitHub workflow runs tests and dry-run only. It never passes `--apply` automatically.


## Alternative-source research — round 2

- `food-alternative-research-round2.md`: additional source review for cooked lean lamb, Doogh, Sangak, Barbari, and Lavash.
- Research-only: not consumed by enrichment, publication, meal aggregation, or the nutrition UI. No food-bank values were changed.


## Alternative-source research — round 3

- `food-alternative-research-round3.md`: primary-table verification for Doogh and Iranian breads, including a correction to a secondary-review citation.
- `food-alternative-sources-round3.json`: structured research-only observations with sample counts, methods, units, caveats, and explicit non-publication status.
- These files are isolated from enrichment and meal aggregation. No food-bank values were changed.

## Alternative-source research archive

These research files are deliberately separate from the food bank and cannot be consumed by the enrichment or publication pipeline:

- [Round 1 alternative-source findings](food-alternative-sources.json)
- [Round 2 research report](food-alternative-research-round2.md)
- [Round 3 research report](food-alternative-research-round3.md) and [structured evidence](food-alternative-sources-round3.json)
- [Round 4 lamb research report](food-alternative-research-round4.md) and [structured evidence](food-alternative-sources-round4.json)
- [Round 5 lamb and Iranian bread report](food-alternative-research-round5.md) and [structured evidence](food-alternative-sources-round5.json)

- [Round 6 Doogh evidence report](food-alternative-research-round6.md) and [structured evidence](food-alternative-sources-round6.json)

- [Round 7 Iranian bread evidence report](food-alternative-research-round7.md) and [structured evidence](food-alternative-sources-round7.json)

- [Final five-food assessment](food-alternative-final-assessment.md) and [structured final assessment](food-alternative-final-assessment.json)

- [Round 8 source-catalog verification correction](food-alternative-research-round6.md#round-8-verification-correction--national-table-edition-and-access)
- [Final five-food assessment](food-alternative-final-assessment.md) and [structured final assessment](food-alternative-final-assessment.json)


All alternative-source observations remain research-only unless independently reviewed, normalized to an explicit edible-portion basis, and separately approved. No round 4 values were published to the food bank.
