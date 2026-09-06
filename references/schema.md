# Spec schema

One yaml file per client in `specs/`. Compiled by `scripts/compile.py`.

```yaml
client: <slug>              # used for output filename
offer: <one line>           # what they actually sell

intake:
  offer_type: readiness     # readiness | manufacturable
  buying_event_hypothesis: >
    Best inference about what changes in the buyer's world right
    before they buy. Usually NOT verified — see confidence below.
  hypothesis_confidence: inferred   # verified|corroborated|inferred|assumed
  hypothesis_evidence: >
    What the guess rests on. Case studies, their own content,
    category logic. Be specific about the source.
  signal_surface: []        # where the event is publicly visible
  window_length: weeks      # days | weeks | months
  purchase_owner: <title>   # who signs / who champions
  demand_noun: <phrase>     # used in the L5 prompt

discovery:                  # questions for the client, from the guesses
  - <question>

disqualify:                 # L0 — runs first, kills rows cheap
  - id: <snake_case>
    kills: <condition>
    examples: []            # optional, sharpens the Claygent prompt
    detect_via: <sources>   # optional, where to look

fit:                        # L1 — standing conditions, no decay
  required: <condition_id>
  any_of: []                # need at least one

window:                     # L2 — time-bound, decays
  tier_a:                   # window-opening; need >=1 to qualify
    - type: <name>
      tightness: tight      # tight | medium | loose — see research.md
      implies: >            # "a company does X only when Y"
      terms: []             # for keyword types
      titles: []            # for hire types
      excluded: []          # titles too universal to be causal
      lookback_days: 90
  tier_b: []                # supporting
  tier_c: []                # context, never scores alone

penalty:
  - trigger: <condition>
    lookback_months: 6
    points: -30

scoring:                    # optional; defaults shown
  tier_a_points: 40
  tier_a_cap: 80
  tier_b_points: 15
  tier_b_cap: 30
  tier_c_points: 5
  tier_c_cap: 10
  threshold: 55
  recency:
    - {max_days: 30, multiplier: 1.0}
    - {max_days: 60, multiplier: 0.8}
    - {max_days: 90, multiplier: 0.6}

regression:                 # poison pills + expected survivors
  - account: <domain>
    expect: DISQUALIFIED    # DISQUALIFIED | NO_WINDOW | QUALIFIED
    at_layer: <disqualify id>
    rationale_must_cite: <signal type>   # for QUALIFIED rows
```

## Notes

**`excluded` matters.** Titles that are near-universal carry no signal.
VP Engineering and CTO are excluded for Together AI. They would not be
for a devtools offer where an eng leadership change genuinely reshapes
tooling decisions.

**Tier placement is causal, not categorical.** `leadership_hire` is
tier_b for Together AI and tier_a for Ramp. Decide by asking whether that
person's arrival directly causes the purchase.

**Regression grows over time.** Every bad row that reaches production
gets added here.
