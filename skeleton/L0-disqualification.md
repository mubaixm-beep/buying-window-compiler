## L0 — Disqualification

Runs first. Chain every downstream column with `Only run if
Disqualified = false` so dead rows never cost credits.

{{DISQUALIFY_TABLE}}

**Clay implementation:** one Claygent column per check, plus a formula
column combining them into a single `Disqualified` boolean.

{{L0_PROMPTS}}

Treat UNKNOWN as pass-through, not as a kill. An absent signal is not
evidence of absence.
