#!/usr/bin/env python3
"""
compile.py — turn a client spec into a paste-ready Clay build doc.

    python3 scripts/compile.py specs/together-ai.yaml
    python3 scripts/compile.py specs/ramp.yaml --regression

The layer skeleton in skeleton/ never changes. This script fills its
slots from the spec. Slots the templates can't fill deterministically are
left as {{CLAUDE:...}} markers for judgment.
"""

import argparse
import pathlib
import sys

try:
    import yaml
except ImportError:
    sys.exit("Need PyYAML:  pip install pyyaml --break-system-packages")

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKELETON = ROOT / "skeleton"
OUTPUT = ROOT / "output"

DEFAULTS = {
    "tier_a_points": 40, "tier_a_cap": 80,
    "tier_b_points": 15, "tier_b_cap": 30,
    "tier_c_points": 5,  "tier_c_cap": 10,
    "threshold": 55,
    "recency": [
        {"max_days": 30, "multiplier": 1.0},
        {"max_days": 60, "multiplier": 0.8},
        {"max_days": 90, "multiplier": 0.6},
    ],
}


def clean(text):
    """Collapse the folded-scalar newlines yaml leaves behind."""
    return " ".join(str(text).split()) if text else ""


def disqualify_table(checks):
    rows = ["| Check | Kill condition | Detect via |", "|---|---|---|"]
    for c in checks:
        kills = clean(c.get("kills"))
        if c.get("examples"):
            kills += f" — e.g. {', '.join(c['examples'])}"
        rows.append(
            f"| `{c['id']}` | {kills} | {clean(c.get('detect_via', 'company enrichment'))} |"
        )
        if c.get("note"):
            rows.append(f"| | *{clean(c['note'])}* | |")
    return "\n".join(rows)


def signal_lines(signals, tier):
    if not signals:
        return "*(none defined — confirm this is intentional)*"
    out = []
    for s in signals:
        line = f"- **`{s['type']}`**"
        if tier == "a" and s.get("tightness"):
            line += f"  `{s['tightness']}`"
        if s.get("note"):
            line += f" — {clean(s['note'])}"
        out.append(line)
        if s.get("implies"):
            out.append(f"  - *Implies:* {clean(s['implies'])}")
        if s.get("terms"):
            out.append(f"  - Keywords: {', '.join(s['terms'])}")
        if s.get("titles"):
            out.append(f"  - Titles: {', '.join(s['titles'])}")
        if s.get("stages"):
            out.append(f"  - Stages: {', '.join(s['stages'])}")
        if s.get("excluded"):
            out.append(
                f"  - **Excluded:** {', '.join(s['excluded'])} "
                f"— too universal to be causal for this offer"
            )
        if tier == "a" and s.get("lookback_days"):
            out.append(f"  - Lookback: {s['lookback_days']} days (recency multiplier applies)")
        elif s.get("lookback_days"):
            out.append(f"  - Lookback: {s['lookback_days']} days")
    return "\n".join(out)


def recency_table(brackets):
    rows = ["| Age of Tier A signal | Multiplier |", "|---|---|"]
    prev = 0
    for b in brackets:
        start = prev + 1 if prev else 0
        rows.append(f"| {start}–{b['max_days']} days | ×{b['multiplier']} |")
        prev = b["max_days"]
    rows.append(f"| over {prev} days | does not count as Tier A |")
    return "\n".join(rows)


def penalty_table(penalties):
    if not penalties:
        return "*(none defined — what do they buy instead? See intake Q6.)*"
    rows = ["| Trigger | Lookback | Points |", "|---|---|---|"]
    for p in penalties:
        rows.append(
            f"| {clean(p['trigger'])} | {p.get('lookback_months', 6)} months | {p['points']} |"
        )
    return "\n".join(rows)


def regression_table(cases):
    if not cases:
        return "**No regression cases defined.** Add at least two poison pills before publishing."
    rows = ["| Account | Expected | Dies at | Why |", "|---|---|---|---|"]
    for c in cases:
        rows.append(
            f"| {c['account']} | `{c['expect']}` | "
            f"{c.get('at_layer', c.get('rationale_must_cite', '—'))} | "
            f"{clean(c.get('note', ''))} |"
        )
    return "\n".join(rows)


def discovery_section(spec):
    qs = spec.get("discovery", [])
    intake = spec.get("intake", {})
    conf = intake.get("hypothesis_confidence", "assumed")
    body = ["## Discovery — hand this to the client",
            "",
            f"The trigger hypothesis is `{conf}`. Everything in L2 depends on it.",
            "Ask rather than assert:",
            ""]
    if qs:
        body += [f"{i}. {clean(q)}" for i, q in enumerate(qs, 1)]
    else:
        body.append("*(no discovery questions written — add them before "
                    "handing this over)*")
    body += ["", "A correction here rewrites L2 and nothing else. Log it in "
             "`regression/` when it arrives."]
    return "\n".join(body)


def fill(name, mapping):
    text = (SKELETON / name).read_text(encoding="utf-8")
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def load_filled(spec_path):
    """Sidecar specs/<client>.filled.yaml holds saved values for
    {{CLAUDE:...}} judgment markers, keyed by marker name, so a
    recompile doesn't wipe hand-filled prompts."""
    sidecar = spec_path.parent / f"{spec_path.stem}.filled.yaml"
    if not sidecar.exists():
        return {}
    data = yaml.safe_load(sidecar.read_text(encoding="utf-8")) or {}
    return {k: str(v) for k, v in data.items() if v}


def compile_spec(spec, filled=None):
    filled = filled or {}
    unfilled = []

    def marker(key, prompt):
        if filled.get(key):
            return filled[key]
        unfilled.append(key)
        return "{{CLAUDE: " + prompt + "}}"

    sc = {**DEFAULTS, **(spec.get("scoring") or {})}
    intake = spec.get("intake", {})
    w = spec.get("window", {})

    conf = intake.get("hypothesis_confidence", "assumed")
    flag = {"verified": "", "corroborated": "",
            "inferred": "  ⚠ inferred from public evidence, not verified",
            "assumed": "  ⚠ placeholder — needs client confirmation"}.get(conf, "")

    motion_line = f"**Motion:** {spec['motion']}\n" if spec.get("motion") else ""

    header = f"""# {spec['client']} — buying window build

**Offer:** {spec['offer']}
{motion_line}**Offer type:** {intake.get('offer_type', '?')}
**Window length:** {intake.get('window_length', '?')}
**Purchase owner:** {intake.get('purchase_owner', '?')}
**Signal surface:** {', '.join(intake.get('signal_surface', []))}

## Trigger hypothesis

> {clean(intake.get('buying_event_hypothesis') or intake.get('buying_event'))}

**Confidence: `{conf}`**{flag}

{clean(intake.get('hypothesis_evidence', 'No evidence recorded.'))}

This is the single most likely thing in this spec to be wrong. Everything
in L2 rests on it. L0, L1, L4 and L5 do not.

---
"""

    parts = [
        header,
        fill("L0-disqualification.md", {
            "DISQUALIFY_TABLE": disqualify_table(spec.get("disqualify", [])),
            "L0_PROMPTS": marker(
                "L0_PROMPTS",
                "write one Claygent prompt per disqualify check, substituting "
                "each check's own kill condition and detect_via sources; for "
                "an enrichment-only check (e.g. a headcount band) note that "
                "it's a plain field read, not a Claygent call"
            ),
        }),
        fill("L1-fit.md", {
            "FIT_REQUIRED": spec.get("fit", {}).get("required", "{{CLAUDE: define}}"),
            "FIT_ANY_OF": "\n".join(
                f"- `{x}`" for x in spec.get("fit", {}).get("any_of", [])
            ) or "*(none defined)*",
        }),
        fill("L2-window.md", {
            "TIER_A": signal_lines(w.get("tier_a", []), "a"),
            "TIER_B": signal_lines(w.get("tier_b", []), "b"),
            "TIER_C": signal_lines(w.get("tier_c", []), "c"),
        }),
        fill("L3-scoring.md", {
            "TIER_A_POINTS": sc["tier_a_points"], "TIER_A_CAP": sc["tier_a_cap"],
            "TIER_B_POINTS": sc["tier_b_points"], "TIER_B_CAP": sc["tier_b_cap"],
            "TIER_C_POINTS": sc["tier_c_points"], "TIER_C_CAP": sc["tier_c_cap"],
            "THRESHOLD": sc["threshold"],
            "RECENCY_TABLE": recency_table(sc["recency"]),
            "PENALTY_TABLE": penalty_table(spec.get("penalty", [])),
        }),
        fill("L4-evidence.md", {"company": "{{Company Name}}"}),
        fill("L5-adjudication.md", {
            "company": "{{Company Name}}",
            "OFFER": spec["offer"],
            "WINDOW_LENGTH": intake.get("window_length", "90 days"),
            "DEMAND_NOUN": intake.get("demand_noun", "demand for this offer"),
            "CONTEXT_FIELDS": marker(
                "CONTEXT_FIELDS",
                "list the row fields worth passing — size, current "
                "vendors, fit evidence"
            ),
        }),
        discovery_section(spec),
        "## Regression\n\n" + regression_table(spec.get("regression", [])),
        """
---

## Ship checklist

- [ ] Table-level auto-run **off** before building
- [ ] Built in sandbox on 20–30 hand-picked rows
- [ ] Every regression account dies at the expected layer
- [ ] At least one qualified row cites two independent sources
- [ ] All CLAUDE judgment markers filled\n- [ ] Discovery questions sent to the client
- [ ] `Review changes` → **`Publish and don't Run`**
""",
    ]
    return "\n\n---\n\n".join(parts), unfilled


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--regression", action="store_true",
                    help="print only the regression table")
    args = ap.parse_args()

    spec_path = pathlib.Path(args.spec)
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))

    if args.regression:
        print(f"\n{spec['client']} — regression set\n")
        print(regression_table(spec.get("regression", [])))
        return

    if spec.get("intake", {}).get("offer_type") == "manufacturable":
        print("\n  STOP. This spec is marked manufacturable.\n"
              "  The pitch can create the want, so there is no window to detect.\n"
              "  Sell ICP definition and messaging instead.\n"
              "  Override by changing offer_type if you disagree.\n")
        return

    OUTPUT.mkdir(exist_ok=True)
    dest = OUTPUT / f"{spec['client']}-build.md"
    filled = load_filled(spec_path)
    doc, unfilled = compile_spec(spec, filled)
    dest.write_text(doc, encoding="utf-8")

    print(f"wrote {dest.relative_to(ROOT)}  ({len(doc.splitlines())} lines)")
    print(f"{len(unfilled)} judgment slot(s) to fill" +
          (f": {', '.join(unfilled)}" if unfilled else ""))


if __name__ == "__main__":
    main()
