// Umbrella math - pure arithmetic engine, runs in browser and node.
(function(root){
"use strict";
function r0(x){ return Math.round(x); }
function r1(x){ return Math.round(x*10)/10; }
function r2(x){ return Math.round(x*100)/100; }
var DOME = 0.85;       // labeled: a domed canopy covers about 85% of its full circle
var PERSON_M2 = 0.3;   // labeled: dry shoulder space per person
function pos(nums, msg){
  for (var i=0;i<nums.length;i++){ if (!isFinite(nums[i]) || nums[i] <= 0) return { error: msg }; }
  return null;
}
function coverPlan(canopyCm){
  var bad = pos([canopyCm], "the canopy must be positive");
  if (bad) return bad;
  var radiusM = canopyCm / 200;
  var area = Math.PI * radiusM * radiusM * DOME;
  return { areaM2: r2(area), people: Math.floor(area / PERSON_M2) };
}
function dryPlan(canopyCm, bodyCm, driftCm){
  var bad = pos([canopyCm, bodyCm], "canopy and body width must be positive");
  if (bad) return bad;
  if (!isFinite(driftCm) || driftCm < 0) return { error: "the drift must be zero or more" };
  var margin = r0((canopyCm - bodyCm) / 2 - driftCm);
  return { marginCm: margin, dry: margin >= 0 };
}
function yearPlan(lostYear, priceEach){
  var bad = pos([lostYear, priceEach], "losses and price must be positive");
  if (bad) return bad;
  return { monthsEach: r1(12 / lostYear), costYear: r2(lostYear * priceEach) };
}
function plural(n, w){ return n + " " + w + (n === 1 ? "" : "s"); }
function renderCover(r, canopyCm){
  return "A " + canopyCm + " cm canopy covers about " + r.areaM2 + " m² at a labeled 85% dome - dry shoulder space for " + r.people + (r.people === 1 ? " person" : " people") + ".";
}
function renderDry(r, driftCm){
  if (r.dry){
    return "After a labeled " + driftCm + " cm of sideways rain drift you keep " + r.marginCm + " cm" + " of dry margin on each side.";
  }
  return "A labeled " + driftCm + " cm of sideways rain drift eats the margin - you come up " + (-r.marginCm) + " cm" + " short on the windward side.";
}
function renderYear(r, lostYear){
  return "At " + plural(lostYear, "umbrella") + " lost or broken a year, one lasts about " + plural(r.monthsEach, "month") + " and the habit costs about " + r.costYear + " a year.";
}
var api = { coverPlan: coverPlan, dryPlan: dryPlan, yearPlan: yearPlan,
  renderCover: renderCover, renderDry: renderDry, renderYear: renderYear };
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.UmbrellaMath = api;
})(typeof window !== "undefined" ? window : globalThis);
