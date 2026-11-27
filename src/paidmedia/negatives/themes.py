"""Theme vocabularies and per-campaign setup for negative-keyword funneling.

Google does not apply close variants to negative keywords, so every term lists
its plurals and spellings. All terms are matched as whole words.

A campaign's `tiers` are ordered highest priority first. An ad group adds
phrase negatives for the themes in higher tiers (so a search containing a
higher-priority word goes to that theme's ad group). Tiers marked mutual also
negate each other inside the tier (cities, insurance carriers).
"""
import re

VOCAB = {
    # talk therapy
    "therapist": ["therapist", "therapists", "therapy", "therapies"],
    "counseling": ["counseling", "counselling", "counselor", "counselors", "counsellor", "counsellors", "counsel"],
    "psychologist": ["psychologist", "psychologists", "psychology", "psychological"],
    "couples": ["couple", "couples", "couple's", "couples'", "marriage", "married", "marital",
                "relationship", "relationships", "spouse", "husband", "wife"],
    "family": ["family", "families", "parent", "parents", "parenting"],
    "child_teen": ["child", "children", "childrens", "children's", "kid", "kids", "teen", "teens",
                   "teenage", "teenager", "teenagers", "adolescent", "adolescents", "pediatric", "youth"],
    "trauma": ["trauma", "traumatic", "ptsd", "emdr", "abuse"],
    "anx_dep": ["anxiety", "depression", "depressed", "panic", "ocd"],
    "adhd": ["adhd"],
    "christian": ["christian", "faith", "faith based", "biblical", "church"],
    "identity": ["black", "african american", "men", "mens", "men's", "male", "women", "womens",
                 "women's", "female", "postpartum", "lgbtq", "lgbt", "gay"],
    "insurance": ["insurance", "aetna", "cigna", "bcbs", "blue cross", "blue shield", "anthem",
                  "united healthcare", "unitedhealthcare", "uhc", "optum", "humana", "medicare",
                  "medicaid", "priority health", "tricare", "carelon", "lucet"],
    # psychiatry
    "psychiatry": ["psychiatrist", "psychiatrists", "psychiatry", "psychiatric"],
    "child": ["child", "children", "childrens", "children's", "kid", "kids", "pediatric"],
    "teen": ["teen", "teens", "teenage", "teenager", "teenagers", "adolescent", "adolescents", "youth"],
    "aetna": ["aetna"], "cigna": ["cigna"], "anthem": ["anthem"], "humana": ["humana"],
    "medicare": ["medicare"], "tricare": ["tricare"],
    "uhc": ["united healthcare", "unitedhealthcare", "uhc", "optum"],
    "bcbs": ["bcbs", "blue cross", "blue shield"],
}


def city_terms(city: str):
    c = city.lower()
    return sorted({c, c.replace("-", " ")})


def _city_from(name: str):
    m = re.search(r"Loc[:\s-]+\s*(.+?),\s*[A-Z]{2}$", name)
    return m.group(1) if m else None


def michigan_theme(ag_name: str):
    if not (ag_name.startswith("EM | ") or ag_name.startswith("PH | ")):
        return None  # only the new test groups are managed
    rest = ag_name[5:]
    city = _city_from(rest)
    if city:
        return f"city:{city.lower()}"
    return {
        "Svc - Find a Therapist": "therapist", "Svc - Counseling": "counseling",
        "Svc - Psychologist": "psychologist", "Svc - Couples & Marriage": "couples",
        "Svc - Family": "family", "Svc - Child & Teen": "child_teen",
        "Spec - Trauma, PTSD & EMDR": "trauma", "Spec - Anxiety & Depression": "anx_dep",
        "Spec - ADHD": "adhd", "Apprch - Christian": "christian",
        "Spec - Men, Women & Black Therapists": "identity", "Ins - Insurance & Carriers": "insurance",
    }.get(rest)


def california_psych_theme(ag_name: str):
    city = _city_from(ag_name)
    if city:
        return f"city:{city.lower()}"
    if ag_name.startswith("Payers - "):
        return ag_name[len("Payers - "):].lower()
    return {"Service - Psychiatry": "psychiatry", "Service - Child/Psychiatry": "child",
            "Service - Teen/Psychiatry": "teen"}.get(ag_name)


CAMPAIGNS = {
    "GGL_NBD_GSE_Geo_Michigan": {
        "theme_of": michigan_theme,
        "tiers": [("city", True), (["insurance"], False), (["christian"], False), (["identity"], False),
                  (["adhd"], False), (["trauma"], False), (["anx_dep"], False), (["child_teen"], False),
                  (["family"], False), (["couples"], False), (["psychologist"], False),
                  (["therapist"], False), (["counseling"], False)],
    },
    "GGL_NBD_GSE_Psych_GEO_California": {
        "theme_of": california_psych_theme,
        "tiers": [("city", True), (["aetna", "anthem", "bcbs", "cigna", "humana", "medicare", "tricare", "uhc"], True),
                  (["child"], False), (["teen"], False), (["psychiatry"], False)],
    },
}
