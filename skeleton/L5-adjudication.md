## L5 — Adjudication

Runs only when `Qualified = true`. Must be able to return no.

```
You are evaluating whether {{company}} is likely to buy
{{OFFER}} in the next {{WINDOW_LENGTH}}.

Evidence: {L4 JSON}
Company context: {{CONTEXT_FIELDS}}

First decide: is there a genuine buying window?
Consider whether this company would source this externally at
all, whether they supply or self-serve it, and whether anyone
internally owns this decision yet.

If no: return exactly NO_WINDOW and one sentence why.

If yes: lead with the single strongest signal and its date,
then one sentence connecting it to {{DEMAND_NOUN}}. Cite only
what appears in the evidence. Do not assert need the evidence
does not support. Under 45 words.
```

Filter out `NO_WINDOW` rows. Expect 30–50% of scored accounts to fail
this pass. That is the column working, not a tuning problem.

**Never write the conclusion into this prompt.** A prompt ending
"...creating an immediate need for X" removes the model's ability to
disagree and produces identical rationales across unrelated accounts.
