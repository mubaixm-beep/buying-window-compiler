## L-1 — Sourcing

The prompt pasted into Clay's "describe what you'd like to do" box to
build the initial list. Runs once, before any L0–L5 column exists — there
is no `Disqualified` field yet to gate on.

**Paste this into Clay:**

```
{{SOURCING_PROMPT}}
```

**Filters** — cheap, free at list-build time only:

{{SOURCING_FILTERS_TABLE}}

**Deliberately not filtered here** — left for L0 to catch:

{{SOURCING_OMITTED}}

Sourcing filters are **looser than L0 on purpose.** Only headcount,
geography, industry, and funding stage belong here — signals Clay can
resolve without enrichment or a Claygent call. Never pre-filter on
anything L0 disqualifies. If sourcing already excludes what L0 would
kill, the disqualifiers never fire, and there is no way to tell whether
L0 is working or just idle. A slightly wide list is the point.

**Target list size:** a few hundred to a few thousand rows.

L0 should kill **20–50%** of the sourced list. Outside that band:

- **Under 20% killed** — sourcing is too tight, already doing L0's job.
  Loosen the filters.
- **Over 50% killed** — L0 is too soft, or sourcing pulled in an
  obviously wrong population. Check both before touching L0.
