---
name: buying-window-compiler
description: Build buying-window detection models in Clay from a domain alone. Paste a company domain and this researches their offer, infers how their buyers decide, and outputs a full Clay build spec — columns, Claygent prompts, scoring logic, and the "why now" prompt. Use this whenever the user pastes a domain and mentions buying windows, window detection, signal-based targeting, intent scoring, trigger events, "why now" columns, account scoring in Clay, or asks which accounts are in-market for a client's offer. Also use when scoping a new outbound client, or when the user shares a Clay workflow or a scored row for critique.
---

# Buying Window Compiler

**Domain in, hypothesis out.**

Paste a domain. This researches the company from public sources and
outputs a complete Clay build spec for detecting who is in-market for
their offer.

The buying trigger is an **inference from public evidence**, not a
verified fact. It is labelled as such throughout. Everything else — the
disqualifiers, fit conditions, scoring, prompts — is grounded in what
research can actually establish.

## The one rule that governs everything

**A column earns its place only if flipping it to its opposite makes the
reason-to-buy disappear.**

For Vanta, "is B2B" is causal — flip it off and nobody needs SOC 2. For
Together AI, "is B2B SaaS" is a demographic proxy inherited from someone
else's build, and it deletes good accounts. Apply this to every
qualification and fit column before it goes in the spec.

## Workflow

### Step 1 — Research the domain

Search for, in roughly this order:

| Question | Where to look |
|---|---|
| What do they sell, to whom, at what price band? | product, pricing, docs |
| Who are the named competitors and substitutes? | comparison pages, G2, review sites |
| Who supplies this category — could a prospect *be* a supplier? | the category itself |
| What locks a company out? | partner pages, cloud/vendor case studies |
| What does their own marketing say triggers a purchase? | case studies, customer stories |
| Would the client's own product telemetry beat external enrichment? | pricing/plan gating, admin/analytics features, what a self-serve signup already reveals in-product |

**Case studies are the highest-value source.** They usually open with the
customer's situation before buying — the closest public proxy for the
buying event you will find. Read several and look for what repeats.

**Check telemetry before proposing outside-in detection.** If the client
can already see seats added, teams created, usage crossing a plan
ceiling, or a security/admin feature getting hit — a Clay build is a more
expensive way to learn something they already know. That's a reason not
to build at all, or to scope the build to only the segment telemetry
can't reach (e.g. accounts that aren't customers yet, so there is no
in-product signal to read).

State plainly what research could not establish.

### Step 2 — Classify the offer, per motion

Classify **the motion this spec serves, not the company.** A single
company can sell through more than one motion, and they classify
differently. Figma: self-serve/Professional is manufacturable — a
designer tries it and it spreads with no external trigger needed — while
the sales-assisted Organization/Enterprise motion is readiness, gated on
a governance or procurement event. Building one spec for "Figma" and
answering both would have been wrong; the case studies that read as
readiness were all Enterprise-motion stories, and applying that
conclusion to the whole company overstated it.

**Readiness** — the buyer decides when something in their world changes.
Vanta: an enterprise deal stalls on a security questionnaire.

**Manufacturable** — the pitch itself creates the want. Show a founder a
Clay build that triples reply rate and they want it regardless of what
happened this quarter.

Detection is expensive — credits, Claygent calls, a six-layer build,
maintenance as sources break. Only worth it when timing is the binding
constraint.

**State which motion the spec targets, explicitly, in the spec itself.**
If the offer splits across motions, say so and pick the readiness one —
the manufacturable motion doesn't need this build regardless of how much
revenue it drives.

**Manufacturable → stop.** Say so plainly and recommend ICP and messaging
work instead. Do not build a spec to be polite.

**Size the fit/disqualify floor to the motion, not the company's whole
market.** A company with a $12/mo self-serve plan and a $90/mo Enterprise
plan does not have one size floor — self-serve absorbs the low end,
and the readiness motion's floor should sit wherever the sales-assisted
path actually starts (headcount where governance/procurement typically
kicks in), not wherever the company's product technically becomes usable.
Setting it too low pulls in accounts telemetry-driven PLG will already
convert without a signal-based build.

Also stop if the window looks shorter than two weeks (enrichment cadence
loses), or if the TAM is under a few hundred accounts (a human reading
each one beats a scoring engine).

### Step 3 — Form the trigger hypothesis

Write `buying_event_hypothesis` with a confidence level and the evidence
behind it.

Rank candidate Tier A signals by **how tight the causal link is from
outside**:

- **Tight** — near self-proving. A job post naming vLLM means they are
  serving models; nobody hires for inference tooling otherwise.
- **Medium** — strongly implies the need, has alternative explanations.
  A new Controller usually means finance process is being rebuilt.
- **Loose** — correlates without causing. Funding, headcount growth,
  general AI hiring. These belong in Tier C.

Prefer tight links. Without deal data, causal tightness is the only
quality control you have on Tier A.

For each Tier A candidate, write one line on why that signal implies the
purchase. If that line is hard to write, the signal is Tier B or C.

### Step 4 — Lean hard on disqualification

This is where outside-in genuinely wins. Trigger inference is uncertain;
disqualification is verifiable from public sources.

When the trigger is a guess, **precision comes from removing accounts
that cannot buy**, not from tighter scoring. Both known bad rows in
`regression/` were catchable from public information alone.

Push past the obvious competitor list to:

- **Competing supply** — they sell the thing
- **Locked in** — multi-year commitment, co-selling deal, entrenched
  enterprise agreement
- **Self-serving** — built it internally, or runs their own fleet
- **Wrong size** — below the budget floor, above the procurement moat
- **Wrong shape** — services business with no product surface

### Step 5 — Write the sourcing prompt (L-1)

Write `sourcing.description`: the plain-English paragraph that gets
pasted into Clay's "describe what you'd like to do" box to build the
unenriched list, before any L0–L5 column exists.

**Sourcing filters are looser than L0 on purpose.** Only use filters
that are free at list-build time — headcount, geography, industry,
funding stage. Never pre-filter on anything L0 disqualifies. If sourcing
already excludes what L0 would kill, the disqualifiers never fire, and
there is no way left to tell whether L0 is doing anything. A slightly
wide list is the point.

Target a few hundred to a few thousand rows. L0 should then kill
20–50% of them — under that and sourcing is too tight, over it and L0
is too soft (or sourcing pulled the wrong population). Record anything
sourcing deliberately leaves for L0 to catch, and why, in
`deliberately_omitted`.

### Step 6 — Write and compile the spec

Write `specs/<client>.yaml` per `references/schema.md`. Use
`specs/together-ai.yaml` and `specs/ramp.yaml` as worked examples — they
differ on every input, which is the point.

```bash
python3 scripts/compile.py specs/<client>.yaml
```

Emits `output/<client>-build.md`. Fill the `{{CLAUDE:...}}` markers —
Claygent prompt bodies and context fields, where template assembly can't
do the work.

### Step 7 — Hand over the hypothesis as a question

The generated doc carries a **Discovery** section listing what was
inferred rather than verified. Give it to the client as a question:

> "We think your buyers show up after X. Is that what you see?"

That question sells better than a finished answer — it shows you
understood their motion and invites the correction that makes the spec
real.

### Step 8 — Regression and ship

Every spec carries a `regression` block: accounts with expected verdicts
and the layer each should die at.

```bash
python3 scripts/compile.py specs/<client>.yaml --regression
```

Then in Clay:

1. Turn off table-level auto-run first (three dots by table name →
   Auto-Update Columns).
2. Build in **sandbox mode** on 20–30 hand-picked rows including the
   regression accounts.
3. Confirm each poison pill dies at the right layer.
4. `Review changes` → **`Publish and don't Run`**. Never `Publish and
   run` — that fires every column across every row.

Manual overrides and manually added rows do not publish. Rows already run
in sandbox carry results back, so no double credit spend.

## Feedback loop

**The trigger hypothesis is the most likely thing in any spec to be
wrong.** Treat it as provisional until a client corrects it.

When they do — or when a bad row reaches production — update the spec and
log it in `regression/`. After four or five corrected specs, look for
Tier A signal types that recur across offer categories. That is the
reusable IP.

## Layer skeleton

Fixed. Never edited per client. Files in `skeleton/`.

| Layer | Purpose | Decays? | Confidence |
|---|---|---|---|
| L-1 | Sourcing — the Clay list-build prompt, before any column exists | no | high (deterministic filters) |
| L0 | Disqualification — who can never buy | no | **high** (verifiable) |
| L1 | Fit — who could buy, ever | no | **high** (verifiable) |
| L2 | Window — who is buying now | **yes** | **inferred** |
| L3 | Scoring + gate | — | inherits L2 |
| L4 | Evidence extraction (dated, sourced) | — | high |
| L5 | Adjudication, can return NO_WINDOW | — | high |

The fit/window split is by **decay**, not by data source. Sorting by
source is what lets job-board data get counted twice.

## Non-negotiables

- **L0 runs first.** Chain with `Only run if` so dead rows die before
  they cost credits.
- **UNKNOWN in L0 is pass-through, not a kill.** Absent evidence is not
  evidence of absence.
- **Gate, don't sum.** `Qualified = (≥1 Tier A) AND (score ≥ threshold)`.
- **Recency multiplier on Tier A only.** Fit conditions don't decay.
- **No single-source scoring.** Every signal tracing to one dataset is a
  bug, not a strong account.
- **L4 before L5.** Undated claims produce rationales where "recently"
  describes something six months old.
- **L5 must be able to say no.** Never write the conclusion into the
  prompt. A prompt ending "...creating an immediate need for X" produces
  identical rationales across unrelated accounts.

## Reference files

- `references/research.md` — the domain research protocol, source by source
- `references/schema.md` — spec yaml field reference
- `references/failure-modes.md` — bad output and the layer that should
  have caught each one
- `references/intake.md` — the six questions, for when you *do* have
  client access
