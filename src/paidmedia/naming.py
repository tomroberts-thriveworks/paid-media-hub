"""Parse Thriveworks Google campaign names into reporting dimensions.

Examples from the onboarding guide:
  GGL_NBD_GSE_Geo_[State]        GGL_NBD_GSE_BroadMatch_*
  GGL_NBD_GSE_ExactMatch_*       GGL_NBD_PMAX_*
  GGL_BRD_GSE_National           GGL_NBD_DEMANDGEN_TalkTherapy
Parsing is tolerant: unknown pieces come back as None, never an error.
"""
import re
from dataclasses import dataclass
from typing import Optional

STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS",
    "KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY",
    "NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV",
    "WI","WY","DC",
}
DECLINING_STATES = {"VA","MA","GA","TX","PA","MI","CT","CO","NJ","NC"}

BOOKINGS, PROXY, MIXED = "bookings", "proxy", "mixed_directional"


@dataclass(frozen=True)
class CampaignInfo:
    name: str
    brand: Optional[str]          # brand | nonbrand
    channel: Optional[str]        # search | pmax | demandgen
    match_structure: Optional[str]  # geo | broad | exact | national
    tier: Optional[int]           # supply tier (NOT a goal type)
    states: tuple
    service_line: Optional[str]   # talk_therapy | psychiatry
    goal_type: str
    declining_market: bool


def parse_campaign(name: str) -> CampaignInfo:
    tokens = [t for t in re.split(r"[_\-\s]+", name.strip()) if t]
    up = [t.upper() for t in tokens]

    brand = "brand" if "BRD" in up else "nonbrand" if "NBD" in up else None
    channel = ("pmax" if "PMAX" in up else "demandgen" if "DEMANDGEN" in up
               else "search" if "GSE" in up else None)
    match = None
    for key, val in (("EXACTMATCH", "exact"), ("BROADMATCH", "broad"),
                     ("GEO", "geo"), ("NATIONAL", "national")):
        if key in up:
            match = val
            break
    tier = None
    for t in up:
        m = re.fullmatch(r"TIER(\d)", t)
        if m:
            tier = int(m.group(1))
    states = tuple(t for t in up if t in STATES)
    joined = "".join(up)
    service = ("psychiatry" if any(k in joined for k in ("PSYCH", "NP")) and "TALK" not in joined
               else "talk_therapy" if any(k in joined for k in ("TALK", "THERAPY", "COUNSEL"))
               else None)

    if channel == "demandgen":
        goal = MIXED
    elif channel == "search" and match == "exact" and tier == 1:
        goal = PROXY       # only group still bid to proxy goals
    else:
        goal = BOOKINGS

    return CampaignInfo(name, brand, channel, match, tier, states, service, goal,
                        bool(set(states) & DECLINING_STATES))
