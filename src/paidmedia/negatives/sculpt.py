"""Plan (and optionally apply) ad-group negatives that keep themed ad groups on theme.

Three rules, all at ad-group level, only for the groups a campaign config manages:
1. Funneling: phrase negatives for the words of higher-priority themes in the same
   campaign (plus same-tier themes for mutual tiers such as cities and carriers).
2. Exact/phrase twins: a "PH | X" group gets the keywords of "EM | X" as exact
   negatives, so exact searches land in the exact group.
3. Search terms: a recent search term that belongs to another managed theme and is
   not already blocked by rule 1 becomes an exact negative in the group it leaked into.
A negative is never added if it would block one of the group's own keywords.
"""
import re
from dataclasses import dataclass, field

from .themes import VOCAB, city_terms


def norm(text: str) -> str:
    return " ".join(text.lower().replace("-", " ").split())


def has_term(text: str, term: str) -> bool:
    return re.search(r"(?<![\w'])" + re.escape(norm(term)) + r"(?![\w'])", norm(text)) is not None


def terms_of(theme: str):
    return city_terms(theme[5:]) if theme.startswith("city:") else VOCAB[theme]


def tier_of(theme: str, tiers):
    for i, (members, mutual) in enumerate(tiers):
        if members == "city" and theme.startswith("city:"):
            return i, mutual
        if members != "city" and theme in members:
            return i, mutual
    raise KeyError(f"theme {theme!r} is not in any tier")


def outranks(other: str, mine: str, tiers) -> bool:
    """True if `other` takes searches away from `mine` (mine should negate other's words)."""
    to, _ = tier_of(other, tiers)
    tm, mutual = tier_of(mine, tiers)
    return to < tm or (to == tm and mutual and other != mine)


def top_theme(query: str, themes, tiers):
    """Highest-priority managed theme whose words appear in the query, or None."""
    hits = [t for t in themes if any(has_term(query, w) for w in terms_of(t))]
    return min(hits, key=lambda t: tier_of(t, tiers)[0]) if hits else None


@dataclass
class Group:
    name: str
    theme: str
    keywords: list            # [(text, MATCH)] enabled positive keywords
    negatives: set = field(default_factory=set)   # existing {(norm text, MATCH)}
    resource: str = ""


@dataclass
class Neg:
    group: str
    text: str
    match: str
    reason: str


def plan(groups, tiers, search_terms=()):
    """groups: [Group]; search_terms: [(group name, term, clicks, cost)]. Returns (adds, skipped)."""
    themes = sorted({g.theme for g in groups})
    by_name = {g.name: g for g in groups}
    adds, skipped, seen = [], [], set()

    def add(g, text, match, reason, protect_any_match=True):
        key = (g.name, norm(text), match)
        if key in seen or (norm(text), match) in g.negatives:
            return
        own = [k for k, _ in g.keywords]
        if match == "PHRASE" and any(has_term(k, text) for k in own):
            skipped.append(Neg(g.name, text, match, "would block own keyword"))
            return
        # An exact negative only blocks that exact search. For the twin rule it may share text
        # with the group's own phrase keyword (that is the point); never with an own exact keyword.
        protected = {norm(k) for k, m in g.keywords if protect_any_match or m == "EXACT"}
        if match == "EXACT" and norm(text) in protected:
            skipped.append(Neg(g.name, text, match, "is an own keyword"))
            return
        seen.add(key)
        adds.append(Neg(g.name, text, match, reason))

    for g in groups:                                    # rule 1
        for other in themes:
            if other != g.theme and outranks(other, g.theme, tiers):
                for w in terms_of(other):
                    add(g, w, "PHRASE", f"funnel to {other}")
    for g in groups:                                    # rule 2
        if g.name.startswith("PH | "):
            twin = by_name.get("EM | " + g.name[5:])
            for k, m in (twin.keywords if twin else []):
                if m == "EXACT":
                    add(g, k, "EXACT", "exact twin", protect_any_match=False)
    phrase_negs = {}
    for n in adds:
        if n.match == "PHRASE":
            phrase_negs.setdefault(n.group, []).append(n.text)
    for name, term, clicks, cost in search_terms:       # rule 3
        g = by_name.get(name)
        if not g:
            continue
        t = top_theme(term, themes, tiers)
        if not t or t == g.theme:
            continue
        existing_phrase = [txt for txt, m in g.negatives if m == "PHRASE"]
        if any(has_term(term, w) for w in phrase_negs.get(name, []) + existing_phrase):
            continue
        add(g, term, "EXACT", f"search term belongs to {t} ({clicks} clicks, ${cost:.0f})")
    return adds, skipped
