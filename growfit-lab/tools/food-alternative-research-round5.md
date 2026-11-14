# Round 5 — cooked lamb reference table and Tehran bread composition evidence

Review date: 2026-11-14

## Executive outcome

This round located a useful cooked lamb-leg entry in the UK *McCance and Widdowson's Composition of Foods* (sixth summary edition, 2002), and verified a Tehran survey of 777 bread samples collected in 2018. It also verified a published table of Iranian bread proximate composition adapted from the Iranian Food Composition Table.

No values are approved for the GrowFit food bank. The new lamb reference makes the naming issue more concrete: the UK cooked leg entry for lean + fat (240 kcal, 28.1 g protein, 14.2 g fat/100g) is much closer to GrowFit's macro profile (250 kcal, 26 g protein, 16 g fat) than the lean-only roasted leg entry (203 kcal, 29.7 g protein, 9.4 g fat). This is a useful diagnostic clue, not proof that the GrowFit food is leg meat or includes fat. Keep the item unresolved until its source definition is known.

## 1. Cooked lamb — foodId 6

### Reference source

Food Standards Agency. *McCance and Widdowson's The Composition of Foods*, Sixth Summary Edition. 2002. Royal Society of Chemistry / Food Standards Agency.

Full text mirror:
https://safeat.ir/wp-content/uploads/2018/06/the-composition-of-foods.pdf

The table reports composition per 100 g edible portion and identifies sample counts and preparation details for several entries.

### Relevant lamb leg rows

| Entry | Preparation / edible part | n | Water g | Protein g | Fat g | Energy kcal |
|---|---|---:|---:|---:|---:|---:|
| 442 | Whole leg, roasted medium, lean | 10 | 60.5 | 29.7 | 9.4 | 203 |
| 443 | Whole leg, roasted medium, lean and fat | calculated 89% lean / 11% fat | 57.3 | 28.1 | 14.2 | 240 |

The inorganic table for entry 442 (lean roasted leg) reports per 100 g edible portion: sodium 63 mg, potassium 360 mg, calcium 7 mg, magnesium 26 mg, phosphorus 220 mg, iron 1.8 mg, zinc 4.6 mg, selenium 4 µg. The vitamin table reports retinol below trace, vitamin D 0.7 µg, thiamin 0.12 mg, riboflavin 0.29 mg, niacin 6.2 mg, vitamin B6 0.34 mg, vitamin B12 2 µg and folate 2 µg.

These are candidate comparison values only. The item is a UK whole leg roasted medium, not an identified Iranian cut or cooking method. It is not a generic "all cooked lean lamb" record.

### Comparison with GrowFit

GrowFit foodId 6 currently has 250 kcal, protein 26 g, fat 16 g and the Persian name "گوشت گوسفندی لخم (پخته)". Entry 443 is closer in macro profile than entry 442, but entry 443 is explicitly lean-and-fat. Therefore:
- Do not map the food to entry 443 merely because the macros are closer.
- Do not map it to entry 442 merely because the name says lean.
- Do not publish any of the lamb micronutrient values yet.
- Keep the record needs-review and request/locate its original cut, trimming and cooking specification in the source materials.

## 2. Traditional breads — foodIds 27, 28, 29

### Tehran salt survey, 2018 samples

Hadian Z, et al. "Survey of the salt (NaCl) Contents of Traditional Breads in Tehran, 2016–2018: Implication for Public Health." International Journal of Preventive Medicine. 2022;13:91. DOI: 10.4103/ijpvm.IJPVM_338_20.

Full text:
https://pmc.ncbi.nlm.nih.gov/articles/PMC9362750/

- 777 bread samples were randomly collected from Tehran in 2018.
- Samples: Lavash n=281, Sangak n=42, Barbari n=220, Taftoon n=234.
- Salt was measured using the Volhard method.
- The reported basis is explicitly g NaCl per 100 g dry weight, not as-eaten weight.
- 2018 means: Lavash 1.43, Sangak 0.41, Barbari 1.58, Taftoon 1.48 g salt/100g dry weight.
- Large variation was observed, especially among Sangak and Lavash samples.

**Do not convert salt to sodium or dry-weight values to as-eaten values without a documented conversion.** The survey reports moisture basis separately only as dried-sample method; it does not supply a matching moisture conversion for each bread sample in the results table. Keep these values research-only.

### Iranian bread proximate composition table

Kazemi F, et al. "Glycemic Index (GI) Values for Major Sources of Dietary Carbohydrates in Iran." International Journal of Endocrinology and Metabolism. 2020;18(3):e99793. DOI: 10.5812/ijem.99793.

Full text:
https://pmc.ncbi.nlm.nih.gov/articles/PMC7695225/

The authors state that the food-composition information in Table 1 was adapted from the Iranian Food Composition Table. The published per-100g table reports:

| Bread | Water % | Energy kcal | Protein g | Fat g | Total carbohydrate g | Fibre g |
|---|---:|---:|---:|---:|---:|---:|
| Sangak | 33 | 258 | 7.7 | 0.7 | 57.4 | 4.1 |
| Lavash | 24 | 291 | 8.8 | 0.8 | 63.4 | 2.4 |
| Taftoon | 28 | 279 | 8.1 | 0.7 | 61.1 | 2.2 |
| Barbari | 29 | 272 | 8.4 | 0.6 | 59.5 | 2.2 |

These values are useful as a local composition cross-check, not a replacement for GrowFit macros without checking the original food-table edition, flour extraction, product formulation and whether the bread definitions align with the bank. This table does not provide the micronutrients required to resolve the pending records.

## 3. Updated five-food evidence status

| FoodId | Food | New evidence in this round | Decision |
|---:|---|---|---|
| 6 | Cooked lamb | CoFID whole-leg roasted medium lean and lean+fat entries, with macro and micronutrient tables | Research-only; closer macro candidate is lean+fat, conflicting with "lean" label |
| 24 | Doogh | No new direct evidence this round | Research-only; previous limitations remain |
| 27 | Sangak | Tehran salt survey and Iranian FCT-derived proximate table | Research-only; salt is dry-weight and proximate values need source-definition check |
| 28 | Barbari | Tehran salt survey and Iranian FCT-derived proximate table | Research-only; salt is dry-weight and proximate values need source-definition check |
| 29 | Lavash | Tehran salt survey and Iranian FCT-derived proximate table | Research-only; salt is dry-weight and proximate values need source-definition check |

## 4. Publication and data-integrity decision

- No values from this round are added to `micronutrientsPer100g`.
- No food-bank values or meal totals are changed.
- The evidence remains in this research archive only.
- Do not convert NaCl to sodium by an assumed factor for this project without explicit evidence and a reviewed conversion record.
- Do not convert dry-weight bread values to edible-portion values without a matched moisture value and documented calculation.
- Keep null values null; do not substitute zeros or population averages.

## Safety and integrity

This file is research-only. It is not read by enrichment, publishing, meal aggregation or the nutrition UI. It does not approve any values, change the food bank, or modify original GrowFit project files.
