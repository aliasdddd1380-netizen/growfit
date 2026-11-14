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
