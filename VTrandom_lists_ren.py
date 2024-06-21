from __future__ import annotations
import builtins
import renpy
from renpy import persistent
from typing import TypeVar
from collections import OrderedDict
from game.major_game_classes.character_related.Person_ren import Person
import math
T = TypeVar('T')
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -2 python:
"""
#TO DO Make sliders not care about 100% totals only on its row, some rows are %, some are Months/week/turns


VT_Settings = {}
#TO-DO Have the total 100% at the bottom to set the Age Population they wish to see more of.
#TO-DO allow players to choose whatever Ages they wish to see etc.
#TO-DO Don't think there is a weighted list for ages.
VT_AGE_RANGES = {
    "adolescent":   (Person.get_age_floor(), Person.get_age_floor()),
    "young_adult":  (Person.get_age_floor() + 1, 24),
    "early_adult":  (25, 35),
    "middle_adult": (36, 51),
    "late_adult":   (52, 72),
    "senior":       (73, 95),
}

VT_Settings["Population"] = {
    "Adolescent":   ["adolescent",    5, 0],
    "Young Adult":  ["young_adult",  30, 1],
    "Millennial":   ["early_adult",  30, 2],
    "Adult":        ["middle_adult", 20, 3],
    "Middle Age":   ["late_adult",   10, 4],
    "Seniors":      ["senior",        5, 5],
}

#TO DO - recommended already set... might need a button to reload the defaults if they need to?
VT_Settings["Virgin Stats"] = {
    "Adolescent - Oral":    ["adolescent_oral",    100,  0],
    "Adolescent - Vaginal": ["adolescent_vaginal", 100,  1],
    "Adolescent - Anal":    ["adolescent_anal",    100,  2],
    "Young Adult - Oral":   ["young_adult_oral",    30,  3],
    "Young Adult - Vaginal":["young_adult_vaginal", 30,  4],
    "Young Adult - Anal":   ["young_adult_anal",    30,  5],
    "Millennial - Oral":    ["early_adult_oral",    20,  6],
    "Millennial - Vaginal": ["early_adult_vaginal", 20,  7],
    "Millennial - Anal":    ["early_adult_anal",    20,  8],
    "Adult - Oral":         ["middle_adult_oral",   10,  9],
    "Adult - Vaginal":      ["middle_adult_vaginal",10, 10],
    "Adult - Anal":         ["middle_adult_anal",   10, 11],
    "Middle Age - Oral":    ["late_adult_oral",     10, 12],
    "Middle Age - Vaginal": ["late_adult_vaginal",  10, 13],
    "Middle Age - Anal":    ["late_adult_anal",     10, 14],
    "Seniors - Oral":       ["senior_oral",          5, 15],
    "Seniors - Vaginal":    ["senior_vaginal",       5, 16],
    "Seniors - Anal":       ["senior_anal",          5, 17],
}
#TO DO - Pregnancy  BunTimer (weeks in labor) 100% = 9 months x 3.5 weeks x 7 days x 7 turns, max (1544), min(172) 3.5 weeks, recommend(344)
#TO DO - Type of pregnancy Natural / C-Section = 100% so its either 40% natural or 100% natural setting, recommended 50% to choose between them
#To DO -  Postsex (sex wait period due to medical recovery usually 6 weeks).
#TO DO - PostSex max 6 weeks = 6x7x7 = 294 turns, min 2 weeks = 98 turns, recommended 3 weeks=147,
VT_Settings["Pregnancy"] = {
    "Bun in the Oven Timer":    ["VT_BunTimer",      4, 0],
    "Natural Delivery":         ["VT_NatDelivery",   8, 1],
    "C-Section Delivery":       ["VT_CSecDelivery", 15, 2],
    "Post-Sex Timer":           ["VT_Postsex",      20, 3],
    }

# update defaults when not exist
for pref in VT_Settings.values():
    for setting in pref.values():
        if not (getattr(persistent, setting[0]) or isinstance(getattr(persistent, setting[0]), int)):
            setattr(persistent, setting[0], setting[1])

def _vt_build_weighted_list(options_dict: dict[str, list[str | int]], start = None, end = None):
    weighted_list = []
    if start is None:
        start = 0
    if end is None:
        end = len(options_dict)

    pref_dict = OrderedDict(options_dict)
    for idx, x in enumerate(pref_dict):
        if idx < start or idx > end:
            continue
        if getattr(persistent, options_dict[x][0], options_dict[x][1]) > 0:
            weighted_list.append((options_dict[x][0], getattr(persistent, options_dict[x][0], options_dict[x][1])))
    return weighted_list