#!/usr/bin/env python3
"""Enrich GrowFit's extracted food bank with USDA FDC micronutrients.
Requires USDA_API_KEY in the environment. No key or credentials are written to the repository.
Only high-confidence food matches are accepted automatically; ambiguous foods are sent to a review report.
"""
import json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANK_PATH = ROOT / "growfit-lab/inbox/growfit-food-bank.json"
TERMS_PATH = ROOT / "growfit-lab/tools/food-search-terms.json"
REVIEW_PATH = ROOT / "growfit-lab/inbox/growfit-food-bank-review.json"
OVERRIDES_PATH = ROOT / "growfit-lab/tools/food-manual-overrides.json"
API = "https://api.nal.usda.gov/fdc/v1/foods/search"
API_KEY = os.environ.get("USDA_API_KEY", "").strip()
NUTRIENTS = {
    "fiber": (1079, ["fiber, total dietary"], "g"),
    "calcium": (1087, ["calcium, ca"], "mg"),
    "iron": (1089, ["iron, fe"], "mg"),
    "potassium": (1092, ["potassium, k"], "mg"),
    "magnesium": (1090, ["magnesium, mg"], "mg"),
    "zinc": (1095, ["zinc, zn"], "mg"),
    "sodium": (1093, ["sodium, na"], "mg"),
    "vitaminA": (1106, ["vitamin a, rae"], "µg RAE"),
    "vitaminC": (1162, ["vitamin c, total ascorbic acid"], "mg"),
    "vitaminD": (1114, ["vitamin d (d2 + d3)", "vitamin d, d2 + d3"], "µg"),
    "vitaminB12": (1178, ["vitamin b-12", "vitamin b12"], "µg"),
    "folate": (1177, ["folate, total"], "µg"),
}
DATA_TYPES = ["Foundation", "SR Legacy", "FNDDS"]
PREP_TOKENS = {"raw", "cooked", "roasted", "boiled", "baked", "dried", "canned", "powder", "fresh", "grilled", "fried"}

def norm(s):
    s = (s or "").lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())

def score_match(query, description, prep):
    q, d = norm(query), norm(description)
    qt, dt = set(q.split()), set(d.split())
    jaccard = len(qt & dt) / max(1, len(qt | dt))
    seq = SequenceMatcher(None, q, d).ratio()
    score = 0.62 * jaccard + 0.38 * seq
    qprep = {x for x in qt if x in PREP_TOKENS}
    dprep = {x for x in dt if x in PREP_TOKENS}
    if qprep and dprep and not (qprep & dprep):
        score -= 0.22
    return max(0.0, min(1.0, score))

def fetch_candidates(query):
    url = API + "?" + urllib.parse.urlencode({"api_key": API_KEY})
    body = json.dumps({"query": query, "dataType": DATA_TYPES, "pageSize": 15, "pageNumber": 1}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={
        "User-Agent": "GrowFit-Lab/1.0", "Content-Type": "application/json"
    }, method="POST")
    with urllib.request.urlopen(req, timeout=35) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("foods", [])

def nutrient_value(food, key):
    nutrient_id, names, _unit = NUTRIENTS[key]
    for item in food.get("foodNutrients", []):
        nutrient = item.get("nutrient") or {}
        nid = item.get("nutrientId", nutrient.get("id"))
        nname = norm(item.get("nutrientName") or nutrient.get("name") or "")
        value = item.get("value", item.get("amount"))
        if value is None:
            continue
        if nid == nutrient_id or any(n == nname for n in names):
            try:
                return round(float(value), 4)
            except (TypeError, ValueError):
                pass
    return None

def extract_micro(food):
    return {key: nutrient_value(food, key) for key in NUTRIENTS}

def fetch_food_details(fdc_id):
    url = "https://api.nal.usda.gov/fdc/v1/food/" + str(fdc_id) + "?" + urllib.parse.urlencode({"api_key": API_KEY})
    req = urllib.request.Request(url, headers={"User-Agent": "GrowFit-Lab/1.0"})
    with urllib.request.urlopen(req, timeout=35) as response:
        return json.loads(response.read().decode("utf-8"))

def has_any_data(micro):
    return any(v is not None for v in micro.values())

def apply_usda_fields(food, match, micro):
    """Update USDA-owned fields without touching independent nutrient evidence."""
    evidence_before = json.dumps(food.get("nutrientEvidence"), ensure_ascii=False, sort_keys=True)
    food["fdcMatch"] = match
    food["micronutrientsPer100g"] = micro
    food["micronutrientUnits"] = {k: v[2] for k, v in NUTRIENTS.items()}
    evidence_after = json.dumps(food.get("nutrientEvidence"), ensure_ascii=False, sort_keys=True)
    if evidence_before != evidence_after:
        raise RuntimeError("USDA enrichment must not modify nutrientEvidence")

def aggregate_meals(bank):
    for meal in bank.get("meals", []):
        sums = {k: 0.0 for k in NUTRIENTS}
        valid = {k: True for k in NUTRIENTS}
        matched_count = 0
        for ingredient in meal.get("ingredients", []):
            food_id = ingredient.get("foodId")
            if not isinstance(food_id, int) or food_id < 0 or food_id >= len(bank["foods"]):
                for k in valid: valid[k] = False
                continue
            food = bank["foods"][food_id]
            micro = food.get("micronutrientsPer100g") or {}
            grams = float(ingredient.get("grams") or 0)
            if food.get("fdcMatch", {}).get("status") == "accepted":
                matched_count += 1
            else:
                for k in valid: valid[k] = False
            for key in NUTRIENTS:
                value = micro.get(key)
                if value is None:
                    valid[key] = False
                else:
                    sums[key] += float(value) * grams / 100.0
        meal["micronutrients"] = {k: round(sums[k], 3) if valid[k] else None for k in NUTRIENTS}
        meal["micronutrientCoverage"] = {
            "matchedIngredients": matched_count,
            "totalIngredients": len(meal.get("ingredients", [])),
            "status": "complete" if all(valid.values()) else ("partial" if any(valid.values()) else "pending")
        }

def main():
    if not API_KEY:
        print("USDA_API_KEY is not configured; keeping existing safe null values.")
        return 0
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    terms_doc = json.loads(TERMS_PATH.read_text(encoding="utf-8"))
    terms = {x["foodId"]: x for x in terms_doc["foods"]}
    overrides_doc = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8")) if OVERRIDES_PATH.exists() else {"foods": []}
    overrides = {int(x["foodId"]): x for x in overrides_doc.get("foods", [])}
    review = {"schemaVersion": 1, "source": "USDA FoodData Central", "items": []}
    accepted = 0
    for food in bank["foods"]:
        term = terms.get(food["id"])
        if not term:
            continue
        manual = overrides.get(food["id"])
        if manual:
            try:
                detail = fetch_food_details(manual["fdcId"])
                actual_description = detail.get("description", "")
                if norm(actual_description) != norm(manual["expectedDescription"]):
                    raise ValueError("USDA description did not match the reviewed override")
                micro = extract_micro(detail)
                if not has_any_data(micro):
                    raise ValueError("USDA record contains no usable micronutrient values")
                apply_usda_fields(food, {
                    "status": "accepted",
                    "fdcId": manual["fdcId"],
                    "description": actual_description,
                    "dataType": detail.get("dataType"),
                    "confidence": 1.0,
                    "source": "USDA FoodData Central",
                    "mappingMethod": "manual-reviewed",
                    "reviewNote": manual["reason"]
                }, micro)
                accepted += 1
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError, KeyError) as exc:
                review["items"].append({
                    "foodId": food["id"], "foodName": food["name"],
                    "query": term["query"], "manualOverride": manual,
                    "error": str(exc)
                })
            time.sleep(0.12)
            continue
        current = food.get("fdcMatch") or {}
        if current.get("status") == "accepted" and current.get("fdcId"):
            accepted += 1
            continue
        try:
            candidates = fetch_candidates(term["query"])
            ranked = []
            for candidate in candidates:
                desc = candidate.get("description", "")
                sc = score_match(term["query"], desc, term.get("prep", ""))
                type_rank = {"Foundation": 0, "SR Legacy": 1, "FNDDS": 2}.get(candidate.get("dataType"), 3)
                ranked.append((sc, -type_rank, candidate))
            ranked.sort(key=lambda x: (x[0], x[1]), reverse=True)
            best = ranked[0] if ranked else None
            if best:
                sc, _tr, candidate = best
                detail = fetch_food_details(candidate.get("fdcId")) if candidate.get("fdcId") else candidate
                micro = extract_micro(detail)
                # Automatic acceptance requires a strong name/preparation match and usable micronutrient data.
                auto = sc >= 0.84 and has_any_data(micro)
                candidate_info = {
                    "fdcId": candidate.get("fdcId"),
                    "description": candidate.get("description"),
                    "dataType": candidate.get("dataType"),
                    "score": round(sc, 3),
                    "micronutrientsPer100g": micro
                }
                if auto:
                    apply_usda_fields(food, {"status": "accepted", "fdcId": candidate_info["fdcId"],
                        "description": candidate_info["description"], "dataType": candidate_info["dataType"],
                        "confidence": candidate_info["score"], "source": "USDA FoodData Central"}, micro)
                    accepted += 1
                else:
                    food["fdcMatch"] = {"status": "review", "source": "USDA FoodData Central"}
                    review["items"].append({"foodId": food["id"], "foodName": food["name"],
                        "query": term["query"], "bestCandidate": candidate_info,
                        "otherCandidates": [{"fdcId": c.get("fdcId"), "description": c.get("description"),
                            "dataType": c.get("dataType"), "score": round(s, 3)}
                            for s, _r, c in ranked[1:4]]})
            else:
                food["fdcMatch"] = {"status": "not-found", "source": "USDA FoodData Central"}
                review["items"].append({"foodId": food["id"], "foodName": food["name"],
                    "query": term["query"], "bestCandidate": None})
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            review["items"].append({"foodId": food["id"], "foodName": food["name"],
                "query": term["query"], "error": str(exc)})
        time.sleep(0.12)
    # Keep per-food status fields in sync with the actual reference-matching result.
    for food in bank["foods"]:
        match = food.get("fdcMatch") or {}
        if match.get("status") == "accepted":
            food["micronutrientStatus"] = "matched" if has_any_data(food.get("micronutrientsPer100g") or {}) else "matched-no-micronutrient-data"
        elif match.get("status") == "review":
            food["micronutrientStatus"] = "needs-review"
        elif match.get("status") == "not-found":
            food["micronutrientStatus"] = "not-found"
        else:
            food["micronutrientStatus"] = "pending-reference-mapping"

    bank["micronutrientSource"] = {
        "name": "USDA FoodData Central", "accessedBy": "GrowFit enrichment script",
        "nutrientsPer100g": {k: {"unit": v[2]} for k, v in NUTRIENTS.items()},
        "matchingPolicy": "Only high-confidence matches are auto-accepted; ambiguous matches require review.",
        "acceptedFoodCount": accepted, "reviewFoodCount": len(review["items"])
    }
    aggregate_meals(bank)
    BANK_PATH.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REVIEW_PATH.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Accepted {accepted}/{len(bank['foods'])} food matches; {len(review['items'])} need review.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
