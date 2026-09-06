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
