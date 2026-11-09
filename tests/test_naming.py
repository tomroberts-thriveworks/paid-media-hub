from paidmedia.naming import parse_campaign, BOOKINGS, PROXY, MIXED
from paidmedia.metrics import cpb, is_booking_action


def test_geo_abbrev_and_full_name():
    c = parse_campaign("GGL_NBD_GSE_Geo_VA")
    assert (c.brand, c.channel, c.match_structure) == ("nonbrand", "search", "geo")
    assert c.states == ("VA",) and c.declining_market and c.goal_type == BOOKINGS
    assert parse_campaign("GGL_NBD_GSE_Geo_Georgia").states == ("GA",)
    assert parse_campaign("GGL_NBD_GSE_Geo_North Carolina").states == ("NC",)
    assert parse_campaign("GGL_NBD_GSE_Geo_West Virginia").states == ("WV",)


def test_psych_texas():
    c = parse_campaign("GGL_NBD_GSE_Psych_GEO_Texas")
    assert c.service_line == "psychiatry" and c.states == ("TX",) and c.regulation == "high"


def test_usa_lc_names():
    c = parse_campaign("GGL_NBD_GSE_Geo_USA_Therapy_LC")
    assert c.nationwide and c.lc_suffix and c.service_line == "talk_therapy" and not c.states
    p = parse_campaign("GGL_NBD_GSE_Geo _USA_P_Broad_LC")
    assert p.service_line == "psychiatry" and p.match_structure == "broad"
    r = parse_campaign("GGL_NBD_GSE_Region_PsychMedication_LC")
    assert r.match_structure == "region" and r.service_line == "psychiatry"


def test_exact_tier1_is_proxy():
    assert parse_campaign("GGL_NBD_GSE_ExactMatch_Tier1_TX").goal_type == PROXY


def test_exact_tier2_is_bookings():
    assert parse_campaign("GGL_NBD_GSE_ExactMatch_Tier2").goal_type == BOOKINGS


def test_brand_national_pmax_demandgen():
    assert parse_campaign("GGL_BRD_GSE_National").brand == "brand"
    assert parse_campaign("GGL_NBD_PMAX_Tier3").channel == "pmax"
    assert parse_campaign("GGL_NBD_DEMANDGEN_TalkTherapy").goal_type == MIXED


def test_unknown_is_tolerant():
    c = parse_campaign("something odd")
    assert c.brand is None and c.states == ()


def test_cpb():
    assert cpb(500, 2) == 250 and cpb(500, 0) is None
    assert is_booking_action("Event 4 - Scheduled Intake")
    assert not is_booking_action("Phone call lead")
