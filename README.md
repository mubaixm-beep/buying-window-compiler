# buying-window-compiler

**Domain in, hypothesis out.**

Paste a company domain. It researches their offer from public sources and
outputs a paste-ready Clay build spec for detecting who is in-market.

The buying trigger is an inference, labelled as one. The disqualifiers,
fit conditions, and prompts are grounded in verifiable research.

The layer skeleton never changes. Every input does.

## Use

```bash
python3 scripts/compile.py specs/together-ai.yaml
python3 scripts/compile.py specs/ramp.yaml --regression
```

Output lands in `output/<client>-build.md`.

## Layout

```
SKILL.md            Claude Code skill — drives the whole workflow
skeleton/           L0–L5 templates with slots. Never edited per client.
specs/              One yaml per client
scripts/compile.py  Spec -> build doc
references/         Research protocol, schema, failure modes, intake
output/             Generated. Gitignore if you like.
regression/         Notes on accounts that got through and why
```

## New client

1. Paste the domain. Research per `references/research.md`.
2. Manufacturable offer, or window under two weeks, or TAM under a few
   hundred → stop. Say so. Sell messaging work instead.
3. Copy the closest spec in `specs/`, rewrite every value. Label the
   trigger hypothesis with its confidence.
4. Compile, fill the `{{CLAUDE:...}}` slots.
5. Build in Clay sandbox. Run the regression accounts.
6. `Review changes` → `Publish and don't Run`.
7. Send the Discovery questions to the client. Their answer rewrites L2.

If you *do* have client access, `references/intake.md` has the six
questions to ask directly — always better than inferring.

## What's confident and what isn't

| Layer | Confidence |
|---|---|
| L0 disqualification | high — verifiable from public sources |
| L1 fit | high — verifiable |
| **L2 window** | **inferred** — the guess, and the thing to correct |
| L3–L5 | high, but inherit L2's uncertainty |

Precision comes from L0 when the trigger is a guess. Docker and BlackLine
were both catchable from public information alone.

## The rule

A column earns its place only if flipping it to its opposite makes the
reason-to-buy disappear. Everything else is a demographic proxy that
deletes good accounts.

## Two specs, side by side

Compare `together-ai.yaml` and `ramp.yaml`. The skeleton is identical.
Every input differs. Note that `leadership_hire` sits in `tier_b` for
Together AI and `tier_a` for Ramp — same signal type, opposite treatment,
decided by whether that person's arrival causes the purchase.

## Growing it

Every bad row that reaches production becomes a regression case. The
`hyperscaler_lockin` check exists because BlackLine got through without
it. Add the check to the spec, add the account to `regression`, and it
can never regress silently.

After four or five client specs, look for Tier A signal types that recur
across offer categories. That's the reusable IP.
