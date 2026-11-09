from paidmedia.naming import parse_campaign, BOOKINGS, PROXY, MIXED
from paidmedia.metrics import cpb, is_booking_action


def test_geo_state():
    c = parse_campaign("GGL_NBD_GSE_Geo_VA")
    assert (c.brand, c.channel, c.match_structure) == ("nonbrand", "search", "geo")
    assert c.states == ("VA",) and c.declining_market and c.goal_type == BOOKINGS


def test_exact_tier1_is_proxy():
    assert parse_campaign("GGL_NBD_GSE_ExactMatch_Tier1_TX").goal_type == PROXY


def test_exact_tier2_is_bookings():
    assert parse_campaign("GGL_NBD_GSE_ExactMatch_Tier2").goal_type == BOOKINGS


def test_brand_national_pmax_demandgen():
    assert parse_campaign("GGL_BRD_GSE_National").brand == "brand"
    assert parse_campaign("GGL_NBD_PMAX_Tier3").channel == "pmax"
    assert parse_campaign("GGL_NBD_DEMANDGEN_TalkTherapy").goal_type == MIXED


def test_unknown_is_tolerant():
    assert parse_campaign("something odd").brand is None


def test_cpb():
    assert cpb(500, 2) == 250 and cpb(500, 0) is None
    assert is_booking_action("Event 4 - Scheduled Intake")
    assert not is_booking_action("Phone call lead")
