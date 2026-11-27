from paidmedia.negatives.sculpt import Group, plan, top_theme, has_term
from paidmedia.negatives.themes import CAMPAIGNS

MI = CAMPAIGNS["GGL_NBD_GSE_Geo_Michigan"]["tiers"]


def mi_groups():
    return [
        Group("EM | Svc - Find a Therapist", "therapist", [("find a therapist", "EXACT")]),
        Group("PH | Svc - Find a Therapist", "therapist", [("find a therapist", "PHRASE")]),
        Group("PH | Svc - Counseling", "counseling", [("counseling psychologist", "PHRASE")]),
        Group("PH | Svc - Psychologist", "psychologist", [("psychologist and therapist", "PHRASE")]),
        Group("PH | Svc - Couples & Marriage", "couples", [("marriage counseling", "PHRASE")]),
        Group("PH | Loc: Troy, MI", "city:troy", [("marriage counseling troy", "PHRASE")]),
        Group("PH | Loc: Novi, MI", "city:novi", [("therapist novi", "PHRASE")]),
    ]


def negs(adds, group):
    return {(n.text, n.match) for n in adds if n.group == group}


def test_counseling_blocks_therapy_but_not_own_keywords():
    adds, skipped = plan(mi_groups(), MI)
    c = negs(adds, "PH | Svc - Counseling")
    assert ("therapy", "PHRASE") in c and ("marriage", "PHRASE") in c and ("troy", "PHRASE") in c
    assert ("psychologist", "PHRASE") not in c          # own keyword "counseling psychologist"
    assert any(s.group == "PH | Svc - Counseling" and s.text == "psychologist" for s in skipped)


def test_therapist_does_not_block_counseling_but_blocks_higher_themes():
    adds, _ = plan(mi_groups(), MI)
    t = negs(adds, "PH | Svc - Find a Therapist")
    assert ("counseling", "PHRASE") not in t
    assert ("psychologist", "PHRASE") in t and ("couples", "PHRASE") in t


def test_cities_are_mutual_and_couples_yields_to_cities():
    adds, _ = plan(mi_groups(), MI)
    assert ("novi", "PHRASE") in negs(adds, "PH | Loc: Troy, MI")
    assert ("troy", "PHRASE") in negs(adds, "PH | Loc: Novi, MI")
    assert ("troy", "PHRASE") in negs(adds, "PH | Svc - Couples & Marriage")
    assert ("marriage", "PHRASE") not in negs(adds, "PH | Loc: Troy, MI")


def test_exact_twin_and_search_term_leak():
    adds, _ = plan(mi_groups(), MI, [("PH | Svc - Find a Therapist", "counseling near me", 3, 21.0)])
    t = negs(adds, "PH | Svc - Find a Therapist")
    assert ("find a therapist", "EXACT") in t           # exact twin: exact searches go to EM group
    assert ("find a therapist", "EXACT") not in negs(adds, "EM | Svc - Find a Therapist")
    assert ("counseling near me", "EXACT") in t          # leaked lower-priority theme


def test_whole_words_only():
    assert has_term("men therapist", "men") and not has_term("mental health", "men")
    assert top_theme("marriage counseling troy", ["couples", "counseling", "city:troy"], MI) == "city:troy"
