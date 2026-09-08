# Patterns across specs

Read together-ai, ramp, figma, snyk, and securityscorecard side by side.
This is what recurs — the reusable layer a sixth build should start
from, per the feedback loop in SKILL.md ("after four or five corrected
specs, look for Tier A signal types that recur across offer
categories"). Five specs isn't a large sample; treat tier placements
here as strong defaults to challenge, not settled law.

## 1. Recurring Tier A signal types, and what offer they indicate

**Named-incumbent pain — one of two tight-signal families.** Four of
the five specs' tightest signals are proof that a *specific, named*
thing the prospect currently runs is failing them, not a generic "they
might have a problem":

| Spec | Signal | What makes it tight |
|---|---|---|
| figma | `legacy_tool_orphaned` | InVision is fully shut down, Adobe XD is unmaintained — objectively verifiable, no interpretation needed |
| ramp | `competitor_complaint` | a public negative review names the incumbent directly |
| together-ai | `stated_cost_or_latency_pain` | the company itself published the pain, in its own words |

(snyk's `compliance_driver` was originally filed in this table too — see
the reclassification below. It never actually fit: there is no
incumbent in it.)

This only exists as a *tight* signal when the offer has a "replaces X"
story with an externally verifiable X. If the incumbent is generic
("some spreadsheet," "some scanner") rather than named and checkable,
the same idea degrades to medium at best — see `first_infra_hire`
(together-ai) and `cloud_native_migration` (snyk), which gesture at the
same "outgrowing the old way" idea without a checkable named incumbent,
and both sit at medium.

**External forcing events — the second tight family, no incumbent
required.** securityscorecard's `regulatory_deadline` and
`third_party_breach_disclosure` are tight for a different reason than
the family above: there is no product or tool of the prospect's that is
named as failing. What makes them tight is that *someone other than the
prospect sets the timeline* — a regulator (DORA, NYDFS Part 500, SEC
disclosure rules) or a documented, dated incident (the 2026 Xsolis
breach reaching Mayo Clinic and six other hospital systems). The company
has no discretion over when to act, the same property that makes
named-incumbent pain tight, arrived at without any incumbent at all.

This reclassifies snyk's `compliance_driver`, which the first version of
this file filed under "named-incumbent pain" on a stretch — its own
writeup already said "an auditor, not the vendor, is forcing the
timeline," which is this family's definition, not the first one's.
`compliance_driver` and `regulatory_deadline` are the same mechanism (an
external certifying or regulatory body sets a deadline the company must
meet, regardless of what tooling it currently runs) applied to two
different offer categories.

| Spec | Signal | What makes it tight |
|---|---|---|
| snyk | `compliance_driver` | an auditor, not a competitor, sets the deadline |
| securityscorecard | `regulatory_deadline` | a regulator (DORA/NYDFS/SEC), not a competitor, sets the deadline |
| securityscorecard | `third_party_breach_disclosure` | a documented, dated, sourced incident — no incumbent tool named, no discretion over timing once it's public |

The common thread across both families is **discretion, not incumbency**:
a signal is tight when the company can't choose to wait — whether
because something they use just died (family 1) or because someone
outside the company set the clock (family 2). `third_party_breach_
disclosure` sits closest to the boundary between the two: it doesn't
name an incumbent *product*, but it does name a specific, dated, sourced
event, the same verifiability bar family 1 runs on. Treat "external
forcing event, no discretion over timing" as the general test and
"named incumbent failing" as one way to satisfy it, not as two
unrelated ideas — any future tight candidate should be checked against
the general test first, then sorted into whichever family (or neither)
it actually belongs to.

**First functional hire.** Recurs in all five specs — `first_infra_hire`
(together-ai), `leadership_hire` (ramp), `first_design_leader_hire`
(figma), `first_appsec_hire` (snyk), `first_tprm_hire`
(securityscorecard). Indicates offers where a *specific role* exists
mainly to make the build-vs-buy call for this category. Tightness varies
with how narrowly that role's mandate is "go choose this tool" —
`first_appsec_hire` and `first_tprm_hire` are both rated tight because
neither role has any other reason to exist yet; `first_infra_hire` and
`first_design_leader_hire` are medium because the hire could be driven
by other priorities first. See §3 for `leadership_hire` specifically,
which is the one type that changes tier across specs on this same axis.

**Budget event naming the category.** `funding_naming_compute`
(together-ai) and `funding_round` (ramp) — a raise or round explicitly
tied to spend in this category. Always medium, never tight, in both
specs that use it: money is fungible, so "they now have budget" never
graduates past "they might spend it here." Indicates offers priced
against company-level spend growth (infra, finance tooling) rather than
per-seat SaaS or platform contracts (this type doesn't appear in figma,
snyk, or securityscorecard).

**Category-specific technical vocabulary in job posts.** `job_keywords`
appears in together-ai, ramp, and (split into two tiers) figma and snyk;
securityscorecard's `vendor_risk_job_keywords` sits at tier_b, the same
place the weak version of this type lands everywhere else. Indicates
offers where the buyer's team leaves a hiring trail specific enough to
be self-proving. Tight only when the terms are narrow and technical
(together-ai's vLLM/TensorRT-LLM/H100 — nobody posts these without
serving models); weak/tier_b when the terms are generic category
vocabulary a company could post for unrelated reasons (snyk's
`devsecops_job_keywords`: DevSecOps, SCA, SAST; ramp's `job_keywords` —
AP specialist, month-end close — moved here from an earlier, unjustified
tier_a placement, see §3; securityscorecard's `vendor_risk_job_keywords`
— third-party risk, TPRM, SIG questionnaire — written straight to
tier_b from the start, on the same reasoning).

**External forcing event, audit or regulation-gated.** `compliance_driver`
(snyk) and `regulatory_deadline` (securityscorecard) — see the
reclassified family above. Indicates offers that sell into a regulatory
or contractual gate an auditor, regulator, or customer imposes — tight
because the company has no discretion over the timeline. Watch for the
caveat snyk's spec attaches: tight for "will buy something soon," not
tight for "will actually adopt it" — a signal can be a reliable purchase
predictor and a weak fit-quality predictor at the same time.
securityscorecard's CONTEXT_FIELDS carries the same two-part caveat for
`regulatory_deadline`, distinguishing a program built from zero from an
existing program tightening up. Any future compliance- or
regulation-gated offer should carry this caveat explicitly, not treat
"tight" as an all-purpose stamp of quality.

## 2. Recurring L0 check types, and when each applies

| Check type | Appears in | Applies when |
|---|---|---|
| `competing_supply` | all five | always — the first check to write for any spec. The prospect could itself be a vendor in this category. |
| `existing_customer` | figma, snyk, securityscorecard | the client's own product has enough market share that "already bought this" is a real, non-trivial share of your enrichment universe, **and** the client has in-product telemetry that makes re-detecting existing customers via Clay wasteful (see SKILL.md Step 1's telemetry check). Notably **absent from together-ai and ramp** — those specs predate this check being a habit. That's a real gap, not a deliberate call: Together AI and Ramp both plausibly have existing customers who'd re-qualify today. Worth retrofitting. |
| lock-in (`hyperscaler_lockin`, `contract_lock`, `competitor_lockin` ×2) | together-ai, ramp, snyk, securityscorecard | the category is normally bought under a **multi-year contractual commitment** that mechanically blocks switching before renewal — cloud infra, finance platforms, security platforms (both AppSec and, now, TPRM/ratings). **Absent from figma** — seat-based SaaS in figma's category is typically annual, not multi-year, and running two design tools in parallel isn't mutually exclusive the way a multi-year cloud, ERP, or platform commitment is. Whether to add a lock-in check is decided by the "flip test": Adobe Creative Cloud usage was considered and *rejected* as a figma disqualifier for exactly this reason — a company can hold a CC enterprise agreement for brand/marketing and still be a live Figma prospect for product design. Lock-in earns a place only when the category is a single-vendor line item, not merely "uses a competitor's product somewhere." securityscorecard's `competitor_lockin` follows snyk's exact template (a job-post mention alone isn't enough; needs a public multi-year commitment or a named standing-platform claim in a case study) and, like snyk's, shipped with **no citable regression example** — a second data point that this check tends to get written on pattern alone, before research turns up a concrete poison pill. Worth flagging explicitly in any future spec's regression checklist rather than treating it as an occasional gap. |
| size floor | all five (`size_band`, `size_floor` ×4) | always, but the floor is set to **where the sales-assisted motion actually starts**, not where the product becomes technically usable (see SKILL.md's motion-based sizing rule and §4's motion re-examination). together-ai: 15 employees — deliberately *low*, because this motion's real gate is inference usage (via L1 fit), not headcount. ramp: 50 employees — raised because self-serve absorbs the smaller end. figma: 25 employees. snyk: 200 employees / ~50 developers — highest of the four prior specs, because self-serve Free/Team genuinely absorbs everything below that. securityscorecard is the first spec to make the floor itself **conditional** rather than a single number: 500 employees generally, dropping to 100 for a regulated industry or public company. That's not a new mechanic so much as size floor and fit merging at the edge — regulation, not headcount, is what actually pulls a company into needing a formal program early, so the floor has to read industry/public-company status before it reads headcount. Future specs where a regulatory driver exists alongside a headcount-driven one should expect the same conditional shape rather than picking one number and hoping it covers both mechanisms. |
| size ceiling | together-ai (`size_band`, 10000), ramp (`size_ceiling`, 5000 + entrenched Concur) | only when *bigness itself* correlates with a disqualifying condition — together-ai's ceiling exists because huge companies likely run owned infra; ramp's ceiling is really a compound condition (size **and** an entrenched incumbent), not size alone. figma, snyk, and securityscorecard have no ceiling: huge enterprises remain valid ICP in all three — for securityscorecard specifically, a regulated Fortune 100 company is exactly who DORA/NYDFS/SEC apply hardest to, so bigness if anything raises fit rather than disqualifying. Don't add a ceiling by default — derive it from a specific reason big companies can't buy, the same way together-ai and ramp did. |
| `wrong_shape` | securityscorecard only | **first appearance of this check type.** Disqualifies a business *shape* (a professional-services or agency business with no material third-party technology dependency or physical supply chain) rather than any competitive, contractual, or size condition. It doesn't ask "could this account be a competitor" or "are they locked in" — it asks "does this category even apply to a business like this," which none of the first four specs needed because their fit layers already implicitly ruled out shapeless businesses (a company with no engineering function fails snyk's L1 required condition anyway, for instance). Worth checking on future specs whether `wrong_shape`-style reasoning belongs in L0 or is already covered by L1's `required` condition — securityscorecard's L1 `required: has_vendor_or_supply_chain_exposure` arguably overlaps with `wrong_shape` and the two haven't been pressure-tested against each other yet. |

## 3. Same signal type, different tier, different reasoning

**`leadership_hire` — tier_a (ramp) vs tier_b (together-ai).** Both
specs hire into a leadership role; the tier split is the cleanest
illustration of schema.md's own rule ("decide by asking whether that
person's arrival directly causes the purchase"). Ramp's Controller/VP
Finance hire has tooling as one of the first, most concentrated things
they touch — a small function with few responsibilities. Together AI's
VP of AI / Head of ML hire has many plausible reasons to exist that have
nothing to do with an imminent GPU-inference purchase — a much less
concentrated role. Same signal shape, opposite tier, because the
*causal density* of the title differs by offer.

**Job posts naming a specific tool — split by whether the tool is
provably dead.** Figma's `legacy_tool_orphaned` (tier_a, tight — names
InVision/Adobe XD, both objectively discontinued) versus
`legacy_tool_job_mention` (tier_b — names Sketch or Zeplin, both
actively maintained competitors). Identical detection mechanism, same
spec, different tier, purely because one incumbent is dead and the
other is merely a competitor. This is the general rule underneath the
"named-incumbent pain" family in §1: aliveness of the named incumbent is
what moves a signal between tiers, not the presence of a name at all.

**Funding events — consistently medium, the counter-example.** Not
every recurring type drifts across tiers. `funding_naming_compute`
(together-ai) and `funding_round` (ramp) are both tier_a and both
medium, for the same reason in both specs: money is fungible, which
caps the ceiling on how tight a spend-signal can ever be, regardless of
category. Useful as a check against over-fitting §3's lesson — some
signal types have a reasoning that doesn't depend on the offer at all.

**Resolved: ramp's `job_keywords`, `erp_migration`, and
`headcount_surge`** originally carried no `tightness` field, unlike
every tier_a entry in the other three specs at the time. Auditing them
against schema.md's own rule ("if that line is hard to write, the
signal is Tier B or C") found `erp_migration` genuinely tight — a named,
dateable finance-systems project — and it stayed in tier_a. The other
two didn't survive the same test: `job_keywords`'s generic vocabulary
(AP specialist, month-end close) is routine backfill hiring at any
revenue-generating company, and `headcount_surge` is a sharper-threshold
version of exactly the signal SKILL.md names as the canonical loose/
tier_c example. Both moved to tier_b in ramp.yaml rather than getting a
tag that would have papered over the same inconsistency this section
flagged. Lesson for future audits: a missing `tightness` tag is often a
sign the tier itself is wrong, not just the label.

**Resolved (this pass): `compliance_driver`'s family, not its tier.**
securityscorecard's audit didn't move any signal to a different tier —
it moved `compliance_driver` to a different *family* in §1's taxonomy,
after five specs made the pattern (external body sets deadline, no
incumbent involved) visible in a way one instance couldn't. Same lesson
as the `job_keywords`/`headcount_surge` case, one level up: a signal
that technically works can still be filed under the wrong reasoning
until a second, independently-argued instance forces the question.

## 4. What the five trigger hypotheses have in common, structurally

- **None claim `verified` confidence.** Highest is ramp's
  `corroborated`; the rest — together-ai, figma, snyk, and now
  securityscorecard — are `inferred`. Every hypothesis in this compiler
  so far is a guess pending client correction — that's the expected
  steady state, not a gap to close before shipping.

- **Every one hedges across 2–3 candidate triggers, not one.**
  together-ai: cost spike *or* latency incident *or* a fine-tune
  shipping. ramp: new finance leader *or* a raise. figma: a tool dying
  *or* fragmentation *or* first-time design-org scaling. snyk:
  compliance deadline *or* first AppSec hire *or* AI-codegen scale-up.
  securityscorecard: regulatory deadline *or* a vendor-caused breach —
  the narrowest hedge of the five, a straight two-way fork rather than
  three candidates. None commit to a single mechanism — the Tier A list
  operationalizes each candidate as its own signal, and discovery asks
  the client which one actually dominates.

- **`hypothesis_evidence` usually cites the client's own published case
  studies as primary evidence, with the bias caveat stated explicitly in
  the more recent specs** (figma, snyk: "this is pattern-matching across
  curated case studies, not a verified sales-cycle account").
  securityscorecard's `hypothesis_evidence` cites case studies (KION,
  Truist, the semiconductor and healthcare MAX examples) the same way,
  and **initially shipped without the selection-bias caveat** — caught
  in this audit and added retroactively, not written in the first pass.
  The bias itself is structural, not spec-specific: a vendor's own case
  studies are selected for having a clean trigger narrative, which is
  exactly what led to the offer_type correction on figma (Enterprise-
  motion case studies got generalized to the whole company). Any new
  spec drawing primarily on the client's own case studies should carry
  this caveat explicitly from the first draft, not assume it's implied
  or add it only when a later audit asks — securityscorecard is proof
  the habit isn't yet automatic even after two prior specs established
  it.

- **Discovery questions are a mechanical restatement of the hypothesis's
  own hedge**, not independent content. Each spec's discovery list asks
  the client to resolve exactly the fork stated in
  `buying_event_hypothesis`, plus a TAM/segmentation check specific to
  what the spec is least sure of (ramp: what size breaks the
  Amex-plus-spreadsheet setup; figma: how much volume is expansion vs.
  net-new; snyk: whether the self-serve/Enterprise wall is real, and
  whether compliance-theatre deals are visible pre-sale;
  securityscorecard: where the size floor actually sits outside
  regulated industries, and whether the free scorecard-lookup motion
  already converts that segment without a rep).

- **Resolved: motion-scoping was inconsistent across the first four —
  and the record here was wrong about figma until this pass.** All five
  now declare a `motion:` field, but figma's was missing entirely until
  the build-doc reformat needed it to render a "Motion" section and
  surfaced the gap; this file previously and incorrectly claimed figma
  had one "from the start." Its motion (sales-assisted
  Organization/Enterprise, self-serve Professional out of scope) was
  sitting fully worked out in SKILL.md's own classification example the
  whole time — it just never made it into the spec file itself. Lesson:
  a worked example in SKILL.md doesn't guarantee the spec it's drawn
  from actually encodes the same thing; check the artifact, not the
  documentation about it. together-ai and ramp predated
  the offer_type correction that surfaced this need and were
  re-examined against it: both turned out to bundle a self-serve motion
  under a spec that had implicitly assumed one funnel. together-ai's own
  pricing splits PLG/self-serve serverless inference from sales-led
  reserved-capacity and Enterprise contracts — this spec targets the
  latter, and its size floor dropped from 50 to 15 employees because
  headcount is a weak proxy for *this* motion specifically (inference
  spend scales with usage, not headcount — a 20-person AI-native startup
  can outspend a 500-person one; the L1 fit conditions do the real
  qualifying work here, not size). ramp's own site literally separates
  "high-intent users ready to self-serve" from "larger teams that need a
  conversation" — this spec targets the latter, and its floor rose from
  15 to 50 employees because the smaller end is exactly what self-serve
  already absorbs without needing signal-based outbound. securityscorecard
  wrote its motion field from the start (self-serve free scorecard
  lookup vs. demo-gated sales-led platform, targeting net-new logos on
  the latter), the first spec to do so without a retrofit — a sign the
  habit from the offer_type correction is holding. Note the two
  retrofitted floors moved in *opposite* directions for opposite
  reasons — motion-scoping doesn't mean "always raise the floor," it
  means "match the floor to why the sales-assisted motion exists," which
  is a governance/procurement threshold for some offers and a
  usage/spend threshold for others.

- **`scoring.threshold: 55` is identical in all five specs**, and none
  of the five sets a custom `recency` table or per-tier point value —
  every spec still runs on the compiler's bare defaults. That's either a
  sign the defaults are well-chosen, or a sign nobody has pressure-tested
  them yet. Should stop being a coincidence once a spec has actual
  regression results from a real Clay build to tune against — five
  specs in, that's still true of all of them.

## What a sixth build should do with this

1. Write `competing_supply` first, always.
2. Ask the telemetry question from SKILL.md Step 1 before writing
   `existing_customer` — only add it if the client can't see this
   internally and the category has enough market share for it to
   matter.
3. Ask the lock-in "flip test" before writing a lock-in check: does the
   category get bought as a multi-year, mutually-exclusive line item?
   If prospects can run a competitor and this offer side by side
   without contradiction, skip it (figma's Adobe CC precedent). If you
   do write one, budget time to find a real regression example before
   shipping — both specs that have written this check so far (snyk,
   securityscorecard) shipped without one.
4. Set the size floor to where the *target motion's* sales-assisted path
   starts, not the company's whole addressable market — and decide the
   motion explicitly, in writing, before sizing anything. If a
   regulatory or compliance driver exists independent of headcount,
   expect the floor to need a conditional form (securityscorecard's
   500/100 split), not a single number.
5. For every tier_a candidate, run the general test before sorting it
   into a family: **does the company have discretion over the timing?**
   If no, ask why — because something specific and named that they run
   just failed or died (named-incumbent pain), or because someone
   outside the company set the clock regardless of what they run
   (external forcing event: a regulator, an auditor, or a documented
   incident). Both produce tight signals; neither requires the other.
   Only after failing that test does a candidate default to medium
   (plausible but not forced) or tier_c (correlates without forcing
   anything).
6. Add the same explicit case-study-selection-bias caveat to
   `hypothesis_evidence` every time it leans on the client's own
   published stories — don't assume a prior spec's habit carries
   forward automatically; securityscorecard shows it doesn't.
