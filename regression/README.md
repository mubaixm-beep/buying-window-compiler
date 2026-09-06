# Regression log

When a bad row reaches production, it goes here and into the client
spec's `regression` block.

Format:

```
## <account> — <date>
Client: <spec>
Verdict given: QUALIFIED
Verdict correct: DISQUALIFIED
Missing: <the layer or check that should have caught it>
Fix: <what changed in the spec or skeleton>
```

---

## docker.com — together-ai
Verdict given: QUALIFIED
Verdict correct: DISQUALIFIED
Missing: L0 competing_supply
Notes: Sells the runtime substrate agents execute inside. The NanoClaw
partnership was read as AI demand when it is evidence of being a supplier
in this stack. Also surfaced a title parse failure ("Vice President of
Engineering, CTO") and an undated "recently" describing a six-month-old
event.
Fix: added competing_supply to L0; added L4 dated-evidence requirement.

## blackline.com — together-ai
Verdict given: QUALIFIED
Verdict correct: DISQUALIFIED
Missing: L0 hyperscaler_lockin
Notes: Job keywords were a genuine Tier A signal, so scoring worked. But
BlackLine moved to Google Cloud in 2019 specifically for ML/AI capability,
expanded to joint go-to-market in 2022, and was still shipping new GCP
regional deployments in late 2025. Public company, committed spend, data
residency obligations.
Fix: added hyperscaler_lockin, detected via partner pages and press
rather than an employee-count proxy.

## grafana.com — together-ai
Verdict given: QUALIFIED
Verdict correct: QUALIFIED
Notes: First row that should survive. Vendor stack (OpenAI, Anthropic,
Pinecone, Weaviate) is real consumption evidence. Rationale still led with
hiring count instead of the stack, and the thesis was vaguely phrased as
"consolidating inference economics" rather than the sharper argument —
frontier per-token pricing on workloads that run fine on open weights.
Fix: L5 instruction to lead with strongest signal; 45-word cap.
