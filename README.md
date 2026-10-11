# Umbrella math

How much a canopy really covers, the dry margin sideways rain leaves you, and what the lose-two-a-year habit costs. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/umbrellamath/

## The three tools

- **Cover plan** - `coverPlan(canopyCm)`: square meters covered and people sheltered.
- **Dry plan** - `dryPlan(canopyCm, bodyCm, driftCm)`: your dry margin after sideways drift, or how far short you come.
- **Year plan** - `yearPlan(lostYear, priceEach)`: months per umbrella and cost per year.

## Labeled norms (illustrative references, not rules)

- Dome: a canopy covers about 85% of its full circle. Shoulder space: 0.3 m² per person.
- Drift: 15 cm of sideways rain in a breeze. Habit: 1.5 umbrellas lost or broken a year. Your canopy, weather and memory decide the real numbers.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (43 cases, 115 checks)

Regenerate the oracle expectations: `python3 oracle.py`
