# Failure modes

Worked examples. Each is real output from a build missing a layer.

## 1. Conclusion written into the prompt

A "Why Now" prompt ending:

> "...and are expanding enterprise AI features, creating an immediate
> need for dedicated inference infrastructure."

The model has no option to disagree. It fills slots and asserts the
ending. Every account above threshold returns the same rationale.

**Symptom:** outputs are structurally identical across unrelated accounts.
**Fix:** L5 adjudication with a NO_WINDOW escape hatch. Ask whether a
window exists; don't tell the model it does.

## 2. Competing supply not disqualified

> "Docker, Inc is entering a buying window for Together AI now because it
> recently hired a Vice President of Engineering, CTO... partnering with
> NanoClaw... raises the need for scalable model deployment."

Docker sells the runtime substrate agents execute inside. The inference
happens elsewhere. The partnership is evidence Docker is a *supplier* in
this stack, making them a weaker compute buyer, not a stronger one.

Also visible: a title parse failure ("Vice President of Engineering, CTO"
— two titles concatenated), and "recently" describing a six-month-old
event because no date reached the prompt.

**Fix:** L0 `competing_supply`. L4 dated evidence. Title normalization
upstream.

## 3. Locked-in customer of a competing supplier

> "BlackLine is entering a buying window... hiring across six distinct AI
> and AI/ML ops roles, with job language centered on inference and
> fine-tuning."

The job keywords are a genuine Tier A signal — that part worked. But
BlackLine has been on Google Cloud since 2019 specifically to add ML and
AI capability, expanded to joint go-to-market in 2022, and was still
launching new GCP regional deployments in late 2025. A public company
with committed hyperscaler spend and data-residency obligations is not
switching inference on the strength of six job ads.

**Fix:** L0 `hyperscaler_lockin`, detected via partner pages, press
releases, and case studies — not an employee-count proxy.

## 4. Single-source scoring

Leading Signal ("AI job keywords") and Custom Signal ("hiring momentum")
both read the job board. Between them, 55 of 100 points from one dataset.
Add a generic eng leadership hire at 30 and an account clears an 80
threshold with nothing indicating it buys the product.

**Fix:** gate on Tier A rather than summing to a threshold. Cap tiers.
Check that a qualified row cites at least two independent sources.

## 5. Inherited filters from someone else's build

Copying "is B2B SaaS" and "sells to mid-market/enterprise" from a Vanta
build into a Together AI build. For Vanta those are the buying mechanism.
For Together they delete consumer AI apps, gaming, media, healthcare AI,
and AI-native startups — all heavy inference buyers.

**Fix:** the flip test. If reversing the filter doesn't remove the reason
to buy, it's a demographic proxy. Cut it.

## 6. Rationale leads with the weakest evidence

> "...hiring across four AI and backend platform roles... Grafana also
> recently rolled out built-in AI assistance, and its use of OpenAI,
> Anthropic, Pinecone, and Weaviate increases the case..."

The vendor stack is the strongest evidence in that paragraph and it lands
third. Hiring count is Tier C and it opens.

**Fix:** L5 instruction to lead with the single strongest signal and its
date. Cap length so filler ("1,903 employees and 14% growth", "scale to
standardize AI infrastructure") gets squeezed out.

## 7. A job posting was evidence, then it wasn't, and nothing noticed

Opal spec, `first_iam_hire`: Primer.io's "IAM Engineer" posting
(jobs.ashbyhq.com/primer.io/b7c9184a-a9a9-40ce-9751-f795f86beb03) was
read in full and confirmed a genuine internal-access-governance hire —
"standing up dedicated IAM," "access review and certification
campaigns," the works. It qualified the account. On the next pass, the
same URL returned "Job not found."

The role had been filled — ordinary and expected for a signal whose
`lookback_days` window is 90. What wasn't expected: the URL didn't 404.
Ashby serves a removed posting as HTTP 200 with an empty client-rendered
shell — the embedded page data shows `"posting":null`, and "Job not
found" only appears after JavaScript runs. A raw fetch, or a search
engine's cached/indexed copy of the page, still shows the *original*
full posting content, with nothing marking it stale. Cross-checked
against Greenhouse: a removed job there returns a real, honest 404
(`{"status":404,"error":"Job not found"}`) via its own posting API. Two
ATS platforms, two completely different "this is gone" signatures — a
check that only reads the HTTP status code catches one and misses the
other, silently.

**Symptom:** a qualified row's strongest (or only) Tier A evidence is a
role that closed between capture and scoring, and nothing in the pipeline
flags it. The lookback window looks like it's doing the job — 90 days is
"recent" — but a job post can die in days, not months.

**Fix:** `compile.py` now auto-generates a liveness-check column for
every tier_a signal keyed on `titles` (any hire-type signal), gated on
the capture column returning TRUE, and wires it into the L3 gate — the
signal only counts toward `tier_a_count`, and only earns points, if the
liveness check also returns TRUE. The check instructs reading the
company's *current* careers/jobs listing directly, not trusting that a
URL loads and not trusting search-result/cache content, because the
Ashby incident is proof both of those are exactly where the stale
version survives. See `references/schema.md`'s note on the `titles`
field for the mechanism, and `specs/opal.yaml`'s regression block
(`primer.io`, expect `NO_WINDOW` at `l2_first_iam_hire_live`) for this
exact case preserved as a poison pill. Not yet extended to tier_b/tier_c
hire signals — they don't gate `Qualified`, so a stale hit there dilutes
score rather than wrongly opening the gate. Revisit if one causes a bad
row.
