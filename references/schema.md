# Spec schema

One yaml file per client in `specs/`. Compiled by `scripts/compile.py`.

## The filled.yaml sidecar

`specs/<client>.filled.yaml` holds hand-authored per-column build
content that can't be generated from the spec's structured fields
alone — the Clay Action's inputs and its formula/Claygent prompt body.
compile.py reads it automatically on every recompile; a missing entry
becomes a `{{CLAUDE:...}}` marker in the output instead of failing.

```yaml
l0:
  <disqualify id>:
    inputs: /Employee Count, /Industry     # Clay columns this check reads
    body: |                                # formula (free) or Claygent prompt (cheap/search)
      ...

l1:
  <fit condition id>:
    cost: cheap                            # free | cheap | search — L1 conditions
    inputs: /Description                   # don't carry a cost in the spec itself,
    body: |                                # so it's declared here
      ...

CONTEXT_FIELDS: >-                          # feeds the L5 prompt's "Company context" line
  ...
```

L2 signal prompts, the L3 scoring formula, and L4's evidence-extraction
prompt are generated entirely from the spec's own `window`, `scoring`,
and `penalty` fields — they never need a sidecar entry.

```yaml
client: <slug>              # used for output filename
offer: <one line>           # what they actually sell

sourcing:                   # L-1 — the Clay list-build prompts, before any column exists
  segments:                 # one entry per AND-only Clay list — never OR two
    - name: <slug>           # populations together in a single prompt (see notes)
      description: >
        One paragraph, plain English, paste-ready into Clay's "describe
        what you'd like to do" box for THIS segment only. Every
        criterion in it must be concrete and mechanical — explicit
        employee ranges, named industries, named countries — not hedged
        ("large enough to", "plausibly", "weighted toward"). Clay's
        filter builder parses this text directly; hedge words don't map
        to a filter, they map to whatever the builder guesses, almost
        always too broad. Include an explicit ceiling, not just a floor.
      filters:              # cheap, free at list-build time — headcount,
        - <filter>            # geography, industry, funding stage. Nothing else.
                             # Must restate the same numbers/lists as the
                             # description, not looser ones.
      expected_row_count: <n or range>   # what this segment's Clay preview
                                          # should show. >5x means too loose.
  deliberately_omitted:     # L0 checks sourcing must NOT pre-filter on
    - check: <L0 disqualify id>
      why: <why sourcing has to let these through>

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
    cost: free               # free | cheap | search — see notes.
                             # compile.py orders the table by this field.
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
      titles: []            # for hire types — see liveness note below
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

**Any tier_a signal with `titles` set automatically gets a liveness
check — you don't write this, `compile.py` generates it.** A hire-type
signal's evidence is one specific job posting, and postings come down
once the role is filled — often well inside the signal's own
`lookback_days` window. `compile.py` inserts a companion Claygent column
(`l2_<type>_live`) right after the signal's own capture column, gated on
that column returning TRUE, and wires it into L3: the signal only counts
toward `tier_a_count` (and only earns points) if its liveness check also
returns TRUE. See `references/failure-modes.md` #7 for the incident that
motivated this — a real posting (Primer.io's, in the opal spec) went
from open to closed between one research pass and the next, and the
platform serving it (Ashby) returned HTTP 200 for the removed posting
rather than a real 404, so a naive "does the URL 404" check would have
missed it.

This applies only to `titles`-based tier_a signals, not `terms`-only
ones (a keyword/press search across multiple possible sources doesn't
decay the same way a single posting URL does) and not to tier_b/tier_c
(they don't gate `Qualified`, so a stale hit there dilutes score rather
than wrongly opening the gate — a real gap, just a smaller one; worth
revisiting if a tier_b hire signal ever causes a bad row).

**Never OR two segments into one prompt.** Clay's filter builder lets
the loosest branch dominate an OR'd prompt — a "public companies, any
industry" branch has pulled in entertainment, e-learning, and consumer
software alongside the intended financial and healthcare targets, with
no indication in the output that it happened. If two populations need
different logic (different headcount floor, different qualifying
condition), write them as two segments — two separate prompts, two
separate Clay lists, run independently — not one prompt joined by "or."
Union the surviving rows into one table only after each segment's own
L0 pass, which also yields a per-segment kill rate: it tells you which
segment is actually worth sourcing from, information one combined
number would average away.

**"Looser than L0" means which checks, not how precisely stated.**
Sourcing skips the checks L0 exists to run — competing supply, existing
customer, lock-in — because those need a Claygent read of product
pages, press, and case studies, not a list-build filter. It does not
mean a segment's prompt can be vague. Every criterion that *is* in it —
headcount, geography, industry, funding stage — must be concrete: an
explicit number or a named list. If a criterion can't be written that
way, it isn't a sourcing filter; it's an L0 check that hasn't been
written yet.

**Set each segment's band against the client's customer concentration,
not just the offer.** Check `existing_customer`'s named examples (or the
regression set) before picking the floor and ceiling. If the client's
published customers cluster in one segment — a handful of very large,
famous logos — aim that segment's band below the concentration.
Resourcing straight into it produces a list that's disproportionately
already-customers, wasting L0 credits instead of finding net-new
accounts.

**Verify the geography filter after every build, not just at write
time.** Clay has silently expanded a single named country into a much
larger list ("United States" applied as "United States +28 more").
Confirm the filter that actually applied in the Clay UI matches what
was typed, for every segment.

Target list size is a few hundred to a few thousand rows per segment;
L0 should then kill 20–50% of each. Outside that band on any one
segment, suspect that segment's sourcing (too tight) or L0 (too soft)
before touching anything else. If a segment's actual Clay preview comes
back at more than 5x its `expected_row_count`, fix that segment's prompt
before building anything on top of the list.

**L0 checks run cheapest-first, not in spec order.** Each check chains
on every previous one returning false, so `cost` order determines how
many rows reach the expensive checks:

1. `free` — a formula or enrichment-field read (a size band read
   straight off company enrichment). No AI column.
2. `cheap` — a description read (entity type, `wrong_shape`) — one AI
   column classifying text Clay already has, no external search.
3. `search` — a Claygent search, narrow against a known list
   (`existing_customer`) or broad and open-ended (`competing_supply`, a
   lock-in check). Both use this same tag; order narrow before broad by
   writing them in that order in the yaml — `compile.py` sorts by `cost`
   but preserves your order for entries that tie.

Running a broad Claygent search on rows a `cheap` description read
would have killed wastes credits for nothing a cheaper check couldn't
already tell you. An untagged check defaults to `search`.

**`excluded` matters.** Titles that are near-universal carry no signal.
VP Engineering and CTO are excluded for Together AI. They would not be
for a devtools offer where an eng leadership change genuinely reshapes
tooling decisions.

**Tier placement is causal, not categorical.** `leadership_hire` is
tier_b for Together AI and tier_a for Ramp. Decide by asking whether that
person's arrival directly causes the purchase.

**Keyword signals read content, not volume.** Six job posts means the
company is hiring. Six job posts naming specific tooling means they are
building the thing that creates demand. Score the second.

**Fit is a gate, not a score.** It answers "could they ever buy this?"
The window layer answers "are they buying now?" A qualified row with no
fit evidence is the single most common false positive — it means the
whole rationale rests on activity signals with nothing establishing the
company consumes this category at all.

**The gate is the point.** `Qualified = (tier_a_count >= 1) AND
(final_score >= threshold)`. Summing to a threshold without the
tier_a_count clause lets volume signals from a single dataset clear the
bar with nothing establishing purchase intent.

**Regression grows over time.** Every bad row that reaches production
gets added here.
