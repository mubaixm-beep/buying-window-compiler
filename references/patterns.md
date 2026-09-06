# Patterns across specs

Read together-ai, ramp, figma, and snyk side by side. This is what
recurs — the reusable layer a fifth build should start from, per the
feedback loop in SKILL.md ("after four or five corrected specs, look
for Tier A signal types that recur across offer categories"). Four
specs isn't a large sample; treat tier placements here as strong
defaults to challenge, not settled law.

## 1. Recurring Tier A signal types, and what offer they indicate

**Named-incumbent pain — the tightest recurring family.** Every spec's
single tightest signal is proof that a *specific, named* thing the
prospect currently runs is failing them, not a generic "they might have
a problem":

| Spec | Signal | What makes it tight |
|---|---|---|
| figma | `legacy_tool_orphaned` | InVision is fully shut down, Adobe XD is unmaintained — objectively verifiable, no interpretation needed |
| ramp | `competitor_complaint` | a public negative review names the incumbent directly |
| snyk | `compliance_driver` | an auditor, not the vendor, is forcing the timeline |
| together-ai | `stated_cost_or_latency_pain` | the company itself published the pain, in its own words |

This only exists as a *tight* signal when the offer has a "replaces X"
story with an externally verifiable X. If the incumbent is generic
("some spreadsheet," "some scanner") rather than named and checkable,
the same idea degrades to medium at best — see `first_infra_hire`
(together-ai) and `cloud_native_migration` (snyk), which gesture at the
same "outgrowing the old way" idea without a checkable named incumbent,
and both sit at medium.

**First functional hire.** Recurs in all four specs — `first_infra_hire`
(together-ai), `leadership_hire` (ramp), `first_design_leader_hire`
(figma), `first_appsec_hire` (snyk). Indicates offers where a *specific
role* exists mainly to make the build-vs-buy call for this category.
Tightness varies with how narrowly that role's mandate is "go choose
this tool" — `first_appsec_hire` is rated tight because the role has
no other reason to exist yet; `first_infra_hire` and
`first_design_leader_hire` are medium because the hire could be driven
by other priorities first. See §3 for `leadership_hire` specifically,
which is the one type that changes tier across specs on this same axis.

**Budget event naming the category.** `funding_naming_compute`
(together-ai) and `funding_round` (ramp) — a raise or round explicitly
tied to spend in this category. Always medium, never tight, in both
specs that use it: money is fungible, so "they now have budget" never
graduates past "they might spend it here." Indicates offers priced
against company-level spend growth (infra, finance tooling) rather than
per-seat SaaS (this type doesn't appear in figma or snyk).

**Category-specific technical vocabulary in job posts.** `job_keywords`
appears in together-ai, ramp, and (split into two tiers) figma and snyk.
Indicates offers where the buyer's team leaves a hiring trail specific
enough to be self-proving. Tight only when the terms are narrow and
technical (together-ai's vLLM/TensorRT-LLM/H100 — nobody posts these
without serving models); weak/tier_b when the terms are generic category
vocabulary a company could post for unrelated reasons (snyk's
`devsecops_job_keywords`: DevSecOps, SCA, SAST; ramp's `job_keywords`
— AP specialist, month-end close — moved here from an earlier,
unjustified tier_a placement; see §3).

**Certification/audit-gated purchase.** `compliance_driver` (snyk) is
this compiler's first instance of the SKILL.md reference case (Vanta:
"an enterprise deal stalls on a security questionnaire"). Indicates
offers that sell into a regulatory or contractual gate an auditor or
customer imposes — tight because the company has no discretion over
the timeline. Watch for the caveat snyk's spec attaches: tight for "will
buy something soon," not tight for "will actually adopt it" — a signal
can be a reliable purchase predictor and a weak fit-quality predictor at
the same time. Any future compliance-gated offer should carry the same
two-part caveat rather than treating "tight" as an all-purpose stamp of
quality.

## 2. Recurring L0 check types, and when each applies

| Check type | Appears in | Applies when |
|---|---|---|
| `competing_supply` | all four | always — the first check to write for any spec. The prospect could itself be a vendor in this category. |
| `existing_customer` | figma, snyk | the client's own product has enough market share that "already bought this" is a real, non-trivial share of your enrichment universe, **and** the client has in-product telemetry that makes re-detecting existing customers via Clay wasteful (see SKILL.md Step 1's telemetry check). Notably **absent from together-ai and ramp** — those specs predate this check being a habit. That's a real gap, not a deliberate call: Together AI and Ramp both plausibly have existing customers who'd re-qualify today. Worth retrofitting. |
| lock-in (`hyperscaler_lockin`, `contract_lock`, `competitor_lockin`) | together-ai, ramp, snyk | the category is normally bought under a **multi-year contractual commitment** that mechanically blocks switching before renewal — cloud infra, finance platforms, security platforms. **Absent from figma** — seat-based SaaS in figma's category is typically annual, not multi-year, and running two design tools in parallel isn't mutually exclusive the way a multi-year cloud or ERP commitment is. Whether to add a lock-in check is decided by the "flip test": Adobe Creative Cloud usage was considered and *rejected* as a figma disqualifier for exactly this reason — a company can hold a CC enterprise agreement for brand/marketing and still be a live Figma prospect for product design. Lock-in earns a place only when the category is a single-vendor line item, not merely "uses a competitor's product somewhere." |
| size floor | all four (`size_band`, `size_floor` ×3) | always, but the floor is set to **where the sales-assisted motion actually starts**, not where the product becomes technically usable (see SKILL.md's motion-based sizing rule and §4's motion re-examination). together-ai: 15 employees — deliberately *low*, because this motion's real gate is inference usage (via L1 fit), not headcount. ramp: 50 employees — raised because self-serve absorbs the smaller end. figma: 25 employees. snyk: 200 employees / ~50 developers — highest of the four because self-serve Free/Team genuinely absorbs everything below that. The number itself matters less than *which* threshold it's tracking: together-ai's low floor and ramp's higher one are both correctly motion-scoped, just against different underlying mechanics (usage vs. self-serve sufficiency). |
| size ceiling | together-ai (`size_band`, 10000), ramp (`size_ceiling`, 5000 + entrenched Concur) | only when *bigness itself* correlates with a disqualifying condition — together-ai's ceiling exists because huge companies likely run owned infra; ramp's ceiling is really a compound condition (size **and** an entrenched incumbent), not size alone. figma and snyk have no ceiling: huge enterprises remain valid ICP in both categories. Don't add a ceiling by default — derive it from a specific reason big companies can't buy, the same way these two did. |

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

**Resolved:** ramp's tier_a entries for `job_keywords`, `erp_migration`,
and `headcount_surge` originally carried no `tightness` field, unlike
every tier_a entry in the other three specs. Auditing them against
schema.md's own rule ("if that line is hard to write, the signal is
Tier B or C") found `erp_migration` genuinely tight — a named, dateable
finance-systems project — and it stayed in tier_a. The other two didn't
survive the same test: `job_keywords`'s generic vocabulary (AP
specialist, month-end close) is routine backfill hiring at any
revenue-generating company, and `headcount_surge` is a sharper-threshold
version of exactly the signal SKILL.md names as the canonical loose/
tier_c example. Both moved to tier_b in ramp.yaml rather than getting a
tag that would have papered over the same inconsistency this section
flagged. Lesson for future audits: a missing `tightness` tag is often a
sign the tier itself is wrong, not just the label.

## 4. What the four trigger hypotheses have in common, structurally

- **None claim `verified` confidence.** Highest is ramp's
  `corroborated`; the rest are `inferred`. Every hypothesis in this
  compiler so far is a guess pending client correction — that's the
  expected steady state, not a gap to close before shipping.

- **Every one hedges across 2–3 candidate triggers, not one.**
  together-ai: cost spike *or* latency incident *or* a fine-tune
  shipping. ramp: new finance leader *or* a raise. figma: a tool dying
  *or* fragmentation *or* first-time design-org scaling. snyk:
  compliance deadline *or* first AppSec hire *or* AI-codegen scale-up.
  None commit to a single mechanism — the Tier A list operationalizes
  each candidate as its own signal, and discovery asks the client which
  one actually dominates.

- **`hypothesis_evidence` always cites the client's own published case
  studies as primary evidence**, and the more recently written specs
  say so with an explicit bias caveat (figma, snyk: "this is
  pattern-matching across curated case studies, not a verified
  sales-cycle account"). together-ai and ramp lean on the same kind of
  evidence without flagging the selection bias as directly. The bias is
  structural, not spec-specific: a vendor's own case studies are
  selected for having a clean trigger narrative, which is exactly what
  led to the offer_type correction on figma (Enterprise-motion case
  studies got generalized to the whole company). Any new spec drawing
  primarily on the client's own case studies should carry this caveat
  explicitly, not assume it's implied.

- **Discovery questions are a mechanical restatement of the hypothesis's
  own hedge**, not independent content. Each spec's discovery list
  asks the client to resolve exactly the 2–3-way fork stated in
  `buying_event_hypothesis`, plus a TAM/segmentation check specific to
  what the spec is least sure of (ramp: what size breaks the
  Amex-plus-spreadsheet setup; figma: how much volume is expansion vs.
  net-new; snyk: whether the self-serve/Enterprise wall is real, and
  whether compliance-theatre deals are visible pre-sale).

- **Resolved: motion-scoping was inconsistent across the four.** All
  four now declare a `motion:` field. together-ai and ramp predated the
  offer_type correction that surfaced this need and were re-examined
  against it: both turned out to bundle a self-serve motion under a
  spec that had implicitly assumed one funnel. together-ai's own
  pricing splits PLG/self-serve serverless inference from sales-led
  reserved-capacity and Enterprise contracts — this spec targets the
  latter, and its size floor dropped from 50 to 15 employees because
  headcount is a weak proxy for *this* motion specifically (inference
  spend scales with usage, not headcount — a 20-person AI-native
  startup can outspend a 500-person one; the L1 fit conditions do the
  real qualifying work here, not size). ramp's own site literally
  separates "high-intent users ready to self-serve" from "larger teams
  that need a conversation" — this spec targets the latter, and its
  floor rose from 15 to 50 employees because the smaller end is exactly
  what self-serve already absorbs without needing signal-based
  outbound. Note the two floors moved in *opposite* directions for
  opposite reasons — motion-scoping doesn't mean "always raise the
  floor," it means "match the floor to why the sales-assisted motion
  exists," which is a governance/procurement threshold for some offers
  and a usage/spend threshold for others.

- **`scoring.threshold: 55` is identical in all four specs**, and none
  of the four sets a custom `recency` table or per-tier point value —
  every spec runs on the compiler's bare defaults. That's either a sign
  the defaults are well-chosen, or a sign nobody has pressure-tested
  them yet. Should stop being a coincidence once a fifth spec has actual
  regression results to tune against.

## What a fifth build should do with this

1. Write `competing_supply` first, always.
2. Ask the telemetry question from SKILL.md Step 1 before writing
   `existing_customer` — only add it if the client can't see this
   internally and the category has enough market share for it to
   matter.
3. Ask the lock-in "flip test" before writing a lock-in check: does the
   category get bought as a multi-year, mutually-exclusive line item?
   If prospects can run a competitor and this offer side by side
   without contradiction, skip it (figma's Adobe CC precedent).
4. Set the size floor to where the *target motion's* sales-assisted
   path starts, not the company's whole addressable market — and
   decide the motion explicitly, in writing, before sizing anything.
5. For every tier_a candidate, name the specific incumbent or role the
   signal depends on and ask whether it's independently, publicly
   verifiable (dead tool, named auditor, named title) — that's what
   separates this compiler's tight signals from its medium ones, every
   time, across all four specs.
