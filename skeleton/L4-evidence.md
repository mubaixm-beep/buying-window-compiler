## L4 — Evidence extraction

Runs before any prose. Structured, dated, sourced — or omitted.

```
Extract every signal found for {{company}} from the row data.

For each, return an object:
{
  "signal_type": "<one of the defined types>",
  "what_happened": "<one factual clause, no interpretation>",
  "date_YYYY_MM_DD": "<date the event occurred or was published>",
  "source_url": "<url>"
}

Return a JSON array. Rules:
- Omit any signal you cannot attach both a date and a source URL to.
- Do not interpret, infer demand, or connect signals to each other.
- Do not restate the same event under two signal types.
- Return [] if nothing qualifies.
```

This layer exists because undated claims produce rationales where
"recently" describes something six months old, and because an
unsourced claim can't be checked by the rep who has to send the email.

**Also check here:** if every extracted signal shares one `source_url`
domain, flag it. Single-source scoring is a bug.
