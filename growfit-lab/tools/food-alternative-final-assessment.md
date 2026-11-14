# Final assessment — five unresolved GrowFit foods

Review date: 2026-11-14
Research archive: rounds 1–7

## Executive decision

The alternative-source research phase for the five unresolved food records has been consolidated. A substantial set of Iranian and international references has been located and screened. **No alternative micronutrient value is approved for publication at this time.**

This is a positive data-quality outcome: the project now has traceable candidate evidence and explicit reasons for rejecting unsafe mappings, rather than filling gaps with plausible-looking but unverified numbers.

The five foods remain `needs-review`, and their `micronutrientsPer100g` values remain `null`. No food-bank record, meal aggregate, nutrition page, or original GrowFit file was changed during the research rounds.

## 1. Current GrowFit source-bank records

The current verified bank contains 113 foods and 741 prepared meals. There are 108 accepted USDA matches and exactly five records marked `needs-review`. None of the five has published alternative-source provenance.

| FoodId | Food | Current kcal | Protein g | Carbs g | Fat g | Micronutrients |
|---:|---|---:|---:|---:|---:|---|
| 6 | گوشت گوسفندی لخم (پخته) | 250 | 26 | 0 | 16 | null |
| 24 | دوغ | 28 | 1.8 | 2.5 | 1 | null |
| 27 | نان سنگک | 260 | 9 | 52 | 1.5 | null |
| 28 | نان بربری | 270 | 9 | 52 | 2.5 | null |
| 29 | نان لواش | 275 | 9 | 57 | 1.2 | null |

## 2. Final evidence matrix

| Food | Best candidate evidence | Why it is not publishable yet | Final state |
|---|---|---|---|
| Cooked lamb (6) | UK CoFID whole roasted leg lean: 203 kcal, P29.7, F9.4; lean+fat: 240 kcal, P28.1, F14.2. South African cut-specific study gives further comparison. | GrowFit's 250 kcal/P26/F16 is closer to a fattier cut than the lean-only entry, but cut, trimming, animal class and preparation are unknown. Do not infer a food match from macro similarity. Some alternative lamb mineral methods are cautioned by their authors. | needs-review |
| Doogh (24) | 2023 Iranian paper cites the Iranian Food Composition Table (the 2023 paper says 2018; FAO/EuroFIR catalogs the dataset as 2017) and reports Doogh water 93.8 g and sodium 421 mg/100g. 2025 industrial survey: n=6, salt 1.04±0.04 g/100g, moisture 82.71±4.92 g/100g. | The 2023 paper does not identify the exact original food code or whether the Doogh values came from the Iranian table or USDA. Industrial samples vary; the 2021 paper has an unresolved salt-unit inconsistency. | needs-review |
| Sangak (27) | Iranian FCT-derived proximate table: water 33%, energy 258 kcal, P7.7, F0.7, carbohydrate 57.4, fibre 4.1 per 100g. Other studies report Fe/Zn and Na/K. | The FCT row's exact product definition needs checking; the regional Na/K table basis is unclear; salt and several mineral results are dry-weight or have unresolved moisture basis. | needs-review |
| Barbari (28) | Iranian FCT-derived proximate table: water 29%, energy 272 kcal, P8.4, F0.6, carbohydrate 59.5, fibre 2.2 per 100g. Other studies report Fe/Zn, Na/K and salt. | Product/flour definition may differ from GrowFit; dry-weight studies and regional surveys cannot be converted to edible-portion values without matched moisture. | needs-review |
| Lavash (29) | Iranian FCT-derived proximate table: water 24%, energy 291 kcal, P8.8, F0.8, carbohydrate 63.4, fibre 2.4 per 100g. Other studies report Zn, Na/K and salt. | Product/flour definition may differ from GrowFit; moisture and analytical basis vary between studies; no complete validated edible-portion micronutrient profile is available. | needs-review |

## 3. Nutrient-specific publication decisions

### Lamb
- No minerals or vitamins from the UK CoFID or South African lamb references are approved for this GrowFit food until the exact cut and trimming state are established.
- The label "lean" and the current 16 g fat/100g need a source-definition review.
- The UK cooked leg reference is useful for comparison only, not a generic cooked-lamb substitution.

### Doogh
- The 2023 paper's sodium value of 421 mg/100g is a strong research lead because it explicitly cites the Iranian FCT (the 2023 paper says 2018; FAO/EuroFIR catalogs the dataset as 2017) among its nutrition sources, but the exact FCT record is not exposed. Keep it research-only.
- Do not turn reported salt values into sodium values automatically.
- Do not use the 2021 salt result until its mg/L versus g/100mL unit inconsistency is resolved.
- Do not use the 2016 calcium/phosphorus table values; their units and internal consistency are not reliable.

### Sangak, Barbari and Lavash
- The Iranian FCT-derived proximate values are useful for cross-checking macros and moisture, but the exact source row and flour extraction details should be checked before replacing GrowFit macros.
- The 2019 Aalipour bread survey provides sodium and potassium measurements from 451 samples, but the wet/dry basis is not sufficiently explicit for direct normalization.
- The 2022 Tehran salt survey is explicitly dry-weight NaCl and cannot be used as as-eaten sodium.
- The 2005 zinc study reports mg/kg with no confirmed moisture basis in the accessible abstract.
- The 2012 Sangak/Barbari mineral study has unresolved moisture basis.
- The 2023 Isfahan element study is dry-weight and contamination-risk focused; it is not a general food-composition dataset. Toxic contaminants are not nutrient fields.

## 4. What would unlock publication

The remaining blockers are specific and finite:

1. **Lamb:** find the original GrowFit food specification or recipe definition: cut, fat trimming, cooking method and whether values are for cooked edible portion.
2. **Doogh:** obtain the original 2018 Iranian Food Composition Table row/code for Doogh, with its complete nutrient profile and product description. If unavailable, a sufficiently representative laboratory analysis with clear per-100g product basis is needed.
3. **Breads:** obtain the original Iranian FCT rows or a validated laboratory source with explicit as-eaten basis, moisture, flour extraction rate and complete nutrient panel. For studies on dry matter, retain dry-basis evidence unless a matching moisture conversion is documented.

Until these inputs exist, the scientifically correct published value is unknown (`null`), not zero and not a borrowed average.

## 5. Data integrity and workflow status

Verified current food-bank state:
- 113 foods
- 741 prepared meals
- 108 foods with accepted USDA matches
- 5 foods still marked `needs-review`
- 0 foods with published alternative-source provenance
- All five unresolved foods retain `micronutrientsPer100g: null`

The research reports and structured evidence files are stored under `growfit-lab/tools/`. They are not read by the enrichment, publisher, meal aggregation or nutrition UI. The controlled publisher remains dry-run by default; the workflow is configured to test and dry-run, not to publish evidence automatically.

No claim is made here that the GitHub Actions test suite has passed; a successful run has not been verified in this research record.

## 6. Research archive

- [Round 1 alternative-source evidence](food-alternative-sources.json)
- [Round 2 report](food-alternative-research-round2.md)
- [Round 3 report](food-alternative-research-round3.md) and [structured data](food-alternative-sources-round3.json)
- [Round 4 report](food-alternative-research-round4.md) and [structured data](food-alternative-sources-round4.json)
- [Round 5 report](food-alternative-research-round5.md) and [structured data](food-alternative-sources-round5.json)
- [Round 6 report](food-alternative-research-round6.md) and [structured data](food-alternative-sources-round6.json)
- [Round 7 report](food-alternative-research-round7.md) and [structured data](food-alternative-sources-round7.json)



## Round 8 source-catalog verification correction

The national database date is not settled by the secondary paper alone. Zakerian et al. (2023) state that the Iranian Food Composition Table was published by NNFTRI in 2018 and that nutritional facts were extracted from both that table and USDA. FAO and EuroFIR, however, catalog the NNFTRI database as **Iranian Food Composition Table 2017**, and mark access as restricted. The 2023 paper's Doogh sodium value (421 mg/100g) is presented in a ranked summary of foods with high sodium, not as a complete reproducible food record. The original food code and whether the value came from the Iranian table or USDA are not disclosed. This strengthens the decision to leave Doogh unresolved; do not publish 421 mg/100g as an approved GrowFit value.

Authoritative catalog references:
- FAO: https://www.fao.org/food-composition/tables-and-databases/detail/%28iran--2017%29-iranian-food-composition-table/en
- EuroFIR: https://www.eurofir.org/food-information/food-composition-databases/
- Primary article text: https://pmc.ncbi.nlm.nih.gov/articles/PMC10811537/
