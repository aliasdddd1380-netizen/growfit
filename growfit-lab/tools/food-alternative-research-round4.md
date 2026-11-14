# Round 4 — lamb composition and reference-database review

Review date: 2026-11-14

## Executive outcome

This round inspected the original South African lamb composition study and its companion food-composition tables, checked the official South African Food Data System (SAFOODS), and verified the UK CoFID 2021 reference dataset.

**No lamb micronutrient values are approved for the GrowFit food bank.** The strongest new finding is that the GrowFit source record is named "گوشت گوسفندی لخم (پخته)" (cooked lean lamb), but its existing macros (250 kcal, protein 26 g, fat 16 g per 100 g) do not describe the clearly trimmed lean leg values in the 2012 South African study. They appear closer to a fattier cooked lamb reference entry, but the exact cut, trim state, animal class and preparation cannot be established from the source record. The label and macro profile therefore need separate review; no automatic remapping is justified.

## 1. GrowFit source record — foodId 6

Current source-bank values per 100 g:
- Name: گوشت گوسفندی لخم (پخته)
- Energy: 250 kcal
- Protein: 26 g
- Carbohydrate: 0 g
- Fat: 16 g
- Micronutrients: null
- Existing match status: needs-review

The word "لخم" normally signals lean meat, but 16 g fat/100 g is not consistent with the 2012 study's cooked lean lamb leg after subcutaneous fat removal (7.67 g fat/100 g). The current macro values should not be silently replaced: the original recipe/food definition may refer to another cut or trim state.

## 2. South African primary study and food tables

Primary research chapter:
van Heerden SM, Schönfeldt HC, Kruger R, Smit MF. "The Nutrient Composition of South African Lamb (A2 Class)." University of Pretoria / Agricultural Research Council research chapter. Full text:
https://repository.up.ac.za/bitstream/handle/2263/25571/04chapter4.pdf

Companion reference booklet:
Schönfeldt HC, Hall N, van Heerden SM. *The Nutrient Content of South African Lamb & Mutton*. June 2012.
https://static1.squarespace.com/static/564312e0e4b02d0ff72509f3/t/5b112e56f950b7d96785f3f4/1527852681536/The%2BNutrient%2BContent%2Bof%2BSA%2BLamb%2B%26%2BMutton%2BMeat.pdf

### Sample and methods context

- The study used A2-class Dorper and Mutton Merino lambs from three South African production areas.
- Six samples were used for each cut in the cooked comparison tables (n=6).
- Shoulder, loin and leg were studied; leg and loin were prepared with dry heat.
- The work distinguishes meat + fat edible portion from lean edible portion with subcutaneous fat removed. These definitions must not be conflated.
- The authors discuss effects of breed, age/fatness class, trimming, cut, cooking method and moisture loss on nutrient composition.

### Selected cooked lamb-leg values per 100 g

| Reference definition | Energy | Protein | Fat | Important interpretation |
|---|---:|---:|---:|---|
| Table 3.4: cooked edible portion, meat + fat | 842 kJ (~201 kcal) | 24.1 g | 11.7 g | Edible portion includes meat and associated fat |
| Table 3.6: cooked lean edible portion | 715 kJ (~171 kcal) | 25.4 g | 7.67 g | Subcutaneous fat removed; not a match for GrowFit's 16 g fat |

These are different food definitions, not competing estimates of the same item. The current GrowFit macro profile (250 kcal / P26 / F16) matches neither row closely enough to prove identity.

### Micronutrient caution

The 2012 booklet explicitly warns that some results are questionable and says iron, zinc and B-vitamin methods may have been inconsistent. The companion research chapter also reports that nutrient profiles differ by cut and cooking state. Therefore, even though the tables provide iron, zinc, magnesium, potassium, sodium and B-vitamin observations, these are retained as research-only pending independent corroboration and exact food-definition matching. Values must not be imported wholesale.

## 3. Broader reference datasets checked

### SAFOODS (South African Food Data System)

Official MRC database page:
https://safoods.mrc.ac.za/composition.html

SAFOODS v2023 describes 1,857 food items and presents values per 100 g edible food. The public overview says the searchable composition tool focuses on energy and selected macronutrients (carbohydrate, fat, protein and fibre); it also cautions that natural variation, species, climate, agriculture, processing and storage affect values. This is a useful local reference system, but the public overview alone does not establish a complete micronutrient panel for GrowFit's exact lamb item.

### UK CoFID 2021

Official dataset and user guide:
https://www.gov.uk/government/publications/composition-of-foods-integrated-dataset-cofid

The official dataset includes separate worksheets for proximates, inorganics, vitamins and other nutrient groups, with values generally expressed per 100 g. It is a strong secondary comparison source for generic foods, but a UK lamb cut/preparation is not automatically equivalent to an Iranian recipe ingredient. Exact food code, cut, trimming and cooking description must be checked before any matching decision.

## 4. Five unresolved food records — consolidated status

| GrowFit foodId | Food | Best evidence found so far | Current decision |
|---:|---|---|---|
| 6 | Cooked lamb ("lean") | South African lamb tables; UK CoFID as a further reference dataset | Keep needs-review; source macro definition conflicts with the "lean" label; no micronutrient approval |
| 24 | Doogh | 2016 Tehran product study, n=3 Doogh products | Research-only; macro disagreement and unclear units/basis; calcium/phosphorus rejected |
| 27 | Sangak | 2019 Iranian regional bread study, n=25, plus 2012 bread mineral study with unresolved moisture basis | Research-only; Na/K basis unresolved; no broad micronutrient profile approved |
| 28 | Barbari | 2019 regional study, n=35, plus 2012/2023 studies with dry-basis or moisture limitations | Research-only; Na/K basis unresolved; dry-weight mineral values cannot be used as eaten |
| 29 | Lavash | 2019 regional study, n=29, plus 2012/2023 studies with dry-basis or moisture limitations | Research-only; Na/K basis unresolved; dry-weight mineral values cannot be used as eaten |

## 5. Publication decision and next evidence needed

- Keep all five foods in needs-review.
- Do not populate `micronutrientsPer100g` from this research round.
- Do not alter existing GrowFit macro values without the original source definition or a documented, approved replacement.
- For lamb, obtain the original GrowFit recipe/food specification: cut, cooked method, whether visible/subcutaneous fat is included, and whether values describe raw or cooked edible portion.
- For breads, obtain a source that explicitly states as-sampled edible-weight basis and reports moisture alongside the nutrient values, or a validated moisture conversion with documented inputs.
- For Doogh, prioritize a representative Iranian food-composition source or a laboratory study with clear per-100g as-consumed units and a credible full nutrient panel.

## Safety and integrity

This file is research-only. It is not read by enrichment, publishing, meal aggregation or the nutrition UI. It does not approve any values, change the food bank, or modify original GrowFit project files.
