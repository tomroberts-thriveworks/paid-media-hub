"""Parse Thriveworks Google campaign names into reporting dimensions.

Real names seen in the optimization tracker:
  GGL_NBD_GSE_Geo_Georgia            (full state name)
  GGL_NBD_GSE_Psych_GEO_Texas        (psychiatry, different token order)
  GGL_NBD_GSE_Geo_USA_Therapy_LC     GGL_NBD_GSE_Geo_USA_LC
  GGL_NBD_GSE_Geo _USA_P_Broad_LC    (note stray space; "P" assumed = psychiatry)
  GGL_NBD_GSE_Region_PsychMedication_LC
  GGL_BRD_GSE_National
Guide patterns: GGL_NBD_GSE_ExactMatch_Tier1, GGL_NBD_PMAX_*, GGL_NBD_DEMANDGEN_TalkTherapy.
Meaning of the "LC" suffix is unknown; it is recorded as a flag only.
Parsing is tolerant: unknown pieces come back as None, never an error.
"""
import re
from dataclasses import dataclass
from typing import Optional

STATE_NAMES = {
    "ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR", "CALIFORNIA": "CA",
    "COLORADO": "CO", "CONNECTICUT": "CT", "DELAWARE": "DE", "FLORIDA": "FL", "GEORGIA": "GA",
    "HAWAII": "HI", "IDAHO": "ID", "ILLINOIS": "IL", "INDIANA": "IN", "IOWA": "IA",
    "KANSAS": "KS", "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
    "MASSACHUSETTS": "MA", "MICHIGAN": "MI", "MINNESOTA": "MN", "MISSISSIPPI": "MS",
    "MISSOURI": "MO", "MONTANA": "MT", "NEBRASKA": "NE", "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH", "NEW JERSEY": "NJ", "NEW MEXICO": "NM", "NEW YORK": "NY",
    "NORTH CAROLINA": "NC", "NORTH DAKOTA": "ND", "OHIO": "OH", "OKLAHOMA": "OK",
    "OREGON": "OR", "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI", "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD", "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT", "VERMONT": "VT",
    "VIRGINIA": "VA", "WASHINGTON": "WA", "WEST VIRGINIA": "WV", "WISCONSIN": "WI",
    "WYOMING": "WY", "DISTRICT OF COLUMBIA": "DC",
}
STATES = set(STATE_NAMES.values())
DECLINING_STATES = {"VA", "MA", "GA", "TX", "PA", "MI", "CT", "CO", "NJ", "NC"}
# Osano opt-in (high-regulation) states per the onboarding guide
HIGH_REG_STATES = {"CA", "CO", "CT", "DE", "IN", "IA", "KY", "MD", "MN", "MT", "NE", "NH",
                   "NJ", "OR", "RI", "TN", "TX", "UT", "VA"}

BOOKINGS, PROXY, MIXED = "bookings", "proxy", "mixed_directional"


@dataclass(frozen=True)
class CampaignInfo:
    name: str
    brand: Optional[str]            # brand | nonbrand
    channel: Optional[str]          # search | pmax | demandgen
    match_structure: Optional[str]  # geo | broad | exact | national | region
    tier: Optional[int]             # supply tier (NOT a goal type)
    states: tuple                   # state abbreviations
    service_line: Optional[str]     # talk_therapy | psychiatry
    goal_type: str
    declining_market: bool
    nationwide: bool = False        # "USA" scope in the name
    lc_suffix: bool = False         # meaning unknown, flag only

    @property
    def regulation(self) -> str:
        """high | low | mixed | unknown, from the states in the name."""
        if not self.states:
            return "unknown"
        hi = [s in HIGH_REG_STATES for s in self.states]
        return "high" if all(hi) else "low" if not any(hi) else "mixed"


def parse_campaign(name: str) -> CampaignInfo:
    # Pull full state names out first (longest first so West Virginia beats Virginia)
    work = " " + re.sub(r"[_\-\s]+", " ", name.strip()).upper() + " "
    states = []
    for full in sorted(STATE_NAMES, key=len, reverse=True):
        pat = f" {full} "
        if pat in work:
            states.append(STATE_NAMES[full])
            work = work.replace(pat, " ", 1)
    tokens = work.split()

    # Abbreviations only count if the original token was written in capitals
    for orig in re.split(r"[_\-\s]+", name.strip()):
        if orig.isupper() and len(orig) == 2 and orig in STATES and orig not in states:
            states.append(orig)

    brand = "brand" if "BRD" in tokens else "nonbrand" if "NBD" in tokens else None
    channel = ("pmax" if "PMAX" in tokens else "demandgen" if "DEMANDGEN" in tokens
               else "search" if "GSE" in tokens else None)
    match = None
    for key, val in (("EXACTMATCH", "exact"), ("BROADMATCH", "broad"), ("BROAD", "broad"),
                     ("REGION", "region"), ("GEO", "geo"), ("NATIONAL", "national")):
        if key in tokens:
            match = val
            break
    tier = next((int(m.group(1)) for t in tokens if (m := re.fullmatch(r"TIER(\d)", t))), None)

    if any(t.startswith("PSYCH") or t in ("P", "NP") for t in tokens):
        service = "psychiatry"
    elif any(t in ("THERAPY", "TALK", "TALKTHERAPY", "COUNSELING") for t in tokens):
        service = "talk_therapy"
    else:
        service = None

    if channel == "demandgen":
        goal = MIXED
    elif channel == "search" and match == "exact" and tier == 1:
        goal = PROXY       # only group still bid to proxy goals
    else:
        goal = BOOKINGS

    return CampaignInfo(name, brand, channel, match, tier, tuple(states), service, goal,
                        bool(set(states) & DECLINING_STATES),
                        nationwide="USA" in tokens, lc_suffix="LC" in tokens)
