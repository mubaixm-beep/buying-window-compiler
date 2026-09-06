## L3 — Scoring and gate

| Tier | Points each | Cap |
|---|---|---|
| A | {{TIER_A_POINTS}} | {{TIER_A_CAP}} |
| B | {{TIER_B_POINTS}} | {{TIER_B_CAP}} |
| C | {{TIER_C_POINTS}} | {{TIER_C_CAP}} |

**Recency multiplier — Tier A only:**

{{RECENCY_TABLE}}

Beyond the final bracket, a signal does not count as Tier A at all.

**Penalties:**

{{PENALTY_TABLE}}

**Gate:**

```
Qualified = (tier_a_count >= 1) AND (final_score >= {{THRESHOLD}})
```

The gate is the point. Summing to a threshold without it lets volume
signals from a single dataset clear the bar with nothing establishing
purchase intent.

**Clay formula syntax:**

```
// Tier A subtotal with recency
MIN({{TIER_A_CAP}},
  SUM(
    IF(days_since_a1 <= 30, {{TIER_A_POINTS}} * 1.0,
    IF(days_since_a1 <= 60, {{TIER_A_POINTS}} * 0.8,
    IF(days_since_a1 <= 90, {{TIER_A_POINTS}} * 0.6, 0)))
  )
)

// Final
final_score = tier_a_subtotal + tier_b_subtotal + tier_c_subtotal + penalties
qualified   = AND(tier_a_count >= 1, final_score >= {{THRESHOLD}})
```
