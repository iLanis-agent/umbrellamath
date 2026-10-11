#!/usr/bin/env python3
"""Python mirror of engine.js - regenerates expected.json. Exact float-for-float mirror."""
import json, math, os

DOME = 0.85
PERSON_M2 = 0.3

def r0(x): return math.floor(x + 0.5)
def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100
def jsnum(x):
    if isinstance(x, float) and x == int(x): return int(x)
    return x
def fmt(x): return repr(jsnum(x))
def pos(nums, msg):
    for n in nums:
        if not (n > 0) or n != n or n == float('inf'): return {"error": msg}
    return None

def coverPlan(canopyCm):
    bad = pos([canopyCm], "the canopy must be positive")
    if bad: return bad
    radiusM = canopyCm / 200
    area = math.pi * radiusM * radiusM * DOME
    return {"areaM2": jsnum(r2(area)), "people": math.floor(area / PERSON_M2)}

def dryPlan(canopyCm, bodyCm, driftCm):
    bad = pos([canopyCm, bodyCm], "canopy and body width must be positive")
    if bad: return bad
    if not (driftCm >= 0) or driftCm != driftCm or driftCm == float('inf'):
        return {"error": "the drift must be zero or more"}
    margin = r0((canopyCm - bodyCm) / 2 - driftCm)
    return {"marginCm": margin, "dry": margin >= 0}

def yearPlan(lostYear, priceEach):
    bad = pos([lostYear, priceEach], "losses and price must be positive")
    if bad: return bad
    return {"monthsEach": jsnum(r1(12 / lostYear)), "costYear": jsnum(r2(lostYear * priceEach))}

def plural(n, w): return fmt(n) + " " + w + ("" if n == 1 else "s")

def renderCover(r, canopyCm):
    return "A " + fmt(canopyCm) + " cm canopy covers about " + fmt(r["areaM2"]) + " m² at a labeled 85% dome - dry shoulder space for " + fmt(r["people"]) + (" person" if r["people"] == 1 else " people") + "."

def renderDry(r, driftCm):
    if r["dry"]:
        return "After a labeled " + fmt(driftCm) + " cm of sideways rain drift you keep " + str(r["marginCm"]) + " cm" + " of dry margin on each side."
    return "A labeled " + fmt(driftCm) + " cm of sideways rain drift eats the margin - you come up " + str(-r["marginCm"]) + " cm" + " short on the windward side."

def renderYear(r, lostYear):
    return "At " + plural(lostYear, "umbrella") + " lost or broken a year, one lasts about " + plural(r["monthsEach"], "month") + " and the habit costs about " + fmt(r["costYear"]) + " a year."

cases = []
cover_args = [100,90,110,120,80,95,105,130,70,115,85,140,0,-50]
for a in cover_args:
    r = coverPlan(a)
    case = {"fn": "coverPlan", "args": [a], "result": r}
    if "error" not in r: case["render"] = renderCover(r, a)
    cases.append(case)
dry_args = [(100,45,15),(110,50,20),(90,45,10),(100,45,27),(100,50,25),(120,55,30),
            (95,48,0),(105,45,18),(100,45,28),(85,42,12),(115,52,22),(100,60,10),
            (0,45,15),(100,45,-5),(100,0,15)]
for a in dry_args:
    r = dryPlan(*a)
    case = {"fn": "dryPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderDry(r, a[2])
    cases.append(case)
year_args = [(1.5,12),(1,10),(2,15),(3,8),(0.5,20),(2.5,11),(4,9),(1,25),
             (6,7),(1.2,14),(0.8,18),(5,6),(0,12),(1.5,0)]
for a in year_args:
    r = yearPlan(*a)
    case = {"fn": "yearPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderYear(r, a[0])
    cases.append(case)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected.json")
with open(out, "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(cases), "cases")
