#!/usr/bin/env python3
"""
compile.py — turn a client spec into a paste-ready Clay build sequence.

    python3 scripts/compile.py specs/together-ai.yaml
    python3 scripts/compile.py specs/ramp.yaml --regression

The layer skeleton in skeleton/ never changes. This script fills its
slots from the spec, generating the mechanical parts (L2 signal
prompts, the L3 scoring formula, gating chains) and pulling
hand-authored per-column content (L0 formulas/prompts, L1 fit prompts,
L5 context fields, doc-level judgment calls) from the spec's
<client>.filled.yaml sidecar. Slots that sidecar can't fill are left as
{{CLAUDE:...}} markers for judgment.

The output doc leads with client-specific context (the offer, the
motion, why this trigger), then says WHAT to build, in order, and HOW
to build each column in Clay: a summary table per step, then a
paste-ready detail block per column in table order. It does not explain
WHY a general rule exists — that lives in SKILL.md and references/.
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

COST_ORDER = {"free": 0, "cheap": 1, "search": 2}
ACTION_LABEL = {
    "free": "`Formula`",
    "cheap": "`AI Column` (web search off)",
    "search": "`Claygent` (web search on)",
}
NUM_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
             6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def clean(text):
    """Collapse the folded-scalar newlines yaml leaves behind."""
    return " ".join(str(text).split()) if text else ""


def block(text):
    """Trim the trailing newline a yaml `|` block scalar leaves behind."""
    return str(text).rstrip("\n") if text else ""


def num_word(n):
    return NUM_WORDS.get(n, str(n))


def title_case(id_str):
    return " ".join(w.capitalize() for w in id_str.split("_"))


def first_sentence(text):
    t = clean(text)
    if not t:
        return ""
    idx = t.find(". ")
    return t[: idx + 1] if idx != -1 else t


def indent(text, prefix="   "):
    return "\n".join((prefix + line if line else "") for line in text.split("\n"))


def fill(name, mapping):
    text = (SKELETON / name).read_text(encoding="utf-8")
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def load_filled(spec_path):
    """Sidecar specs/<client>.filled.yaml holds hand-authored content
    (L0 formulas/prompts, L1 fit prompts, L5 context fields, doc-level
    judgment calls) so a recompile doesn't wipe it. Returned as-is (not
    flattened) so nested per-check dicts (l0, l1) survive."""
    sidecar = spec_path.parent / f"{spec_path.stem}.filled.yaml"
    if not sidecar.exists():
        return {}
    return yaml.safe_load(sidecar.read_text(encoding="utf-8")) or {}


# ---------------------------------------------------------------- L-1 --

def sourcing_segments_block(segments):
    if not segments:
        return "*(no segments defined — write at least one, AND-only, before building)*"
    blocks = []
    for i, seg in enumerate(segments, 1):
        name = seg.get("name", "segment")
        prompt = clean(seg.get("description", "")) or \
            "{{CLAUDE: write this segment's AND-only sourcing prompt}}"
        row_count = seg.get("expected_row_count") or \
            "{{CLAUDE: estimate expected row count}}"
        blocks.append(
            f"**1.{i} {name}** — expect {row_count}\n\n"
            f"```\n{prompt}\n```"
        )
    return "\n\n".join(blocks)


def render_sourcing(sourcing):
    segments = sourcing.get("segments", [])
    n = len(segments)
    intro = ("One list, built once." if n == 1 else
              f"{n} lists, built separately. Never combine into one prompt.")
    return fill("L-1-sourcing.md", {
        "SOURCING_INTRO": intro,
        "SOURCING_SEGMENTS": sourcing_segments_block(segments),
    })


# ----------------------------------------------------------------- L0 --

def output_field(prefix, check_id):
    return f"{prefix}_{check_id}"


def gate_ref(field, cost):
    return f"{field} = false" if cost == "free" else f'{field} != "TRUE"'


def true_ref(field, cost):
    return field if cost == "free" else f'{field} = "TRUE"'


def config_from_kills(c):
    text = clean(c.get("kills", ""))
    if c.get("examples"):
        text += " — " + ", ".join(c["examples"])
    if not text:
        return "See detail block below."
    first = text[0].lower() + text[1:] if len(text) > 1 else text.lower()
    sentence = f"Kills {first}"
    return sentence if sentence.endswith((".", "!", "?")) else sentence + "."


def render_l0(checks, l0_filled):
    ordered = sorted(
        enumerate(checks),
        key=lambda ic: (COST_ORDER.get(ic[1].get("cost"), COST_ORDER["search"]), ic[0]),
    )
    ordered = [c for _, c in ordered]

    table = ["| Column Name | Clay Native Action / Logic | Cost | Configuration |",
              "|---|---|---|---|"]
    blocks = []
    prior_gate_refs = []
    combine_terms = []
    for i, c in enumerate(ordered, 1):
        cid = c["id"]
        cost = c.get("cost", "search")
        info = l0_filled.get(cid, {}) if isinstance(l0_filled, dict) else {}
        inputs = info.get("inputs") or "{{CLAUDE: name the Clay columns this reads}}"
        body = block(info.get("body")) or "{{CLAUDE: write this check's formula or Claygent prompt}}"
        field = output_field("l0", cid)
        only_run_if = "—" if not prior_gate_refs else "AND(" + ", ".join(prior_gate_refs) + ")"
        out_type = "boolean" if cost == "free" else "TRUE / FALSE / UNKNOWN"
        name = title_case(cid)

        table.append(f"| **{name}** | {ACTION_LABEL.get(cost, ACTION_LABEL['search'])} | {cost} | {config_from_kills(c)} |")

        entry = (
            f"### 2.{i} — {name}\n"
            f"**Inputs:** {inputs}\n"
            f"**Only run if:** {only_run_if}\n"
            f"**Output:** {out_type} → `{field}`\n\n"
            f"```\n{body}\n```"
        )
        if c.get("note"):
            entry += f"\n\n> {clean(c['note'])}"
        blocks.append(entry)

        prior_gate_refs.append(gate_ref(field, cost))
        combine_terms.append(true_ref(field, cost))

    n = len(ordered)
    table.append(f"| **Disqualified** | `Formula` | free | "
                  f"Combines all {num_word(n)} checks into one boolean. "
                  f"Everything downstream gates on this. |")
    blocks.append(
        f"### 2.{n + 1} — Disqualified\n"
        f"**Inputs:** all of the above\n"
        f"**Output:** boolean → `Disqualified`\n\n"
        f"```\nOR(\n  " + ",\n  ".join(combine_terms) + "\n)\n```"
    )
    return "\n".join(table) + "\n\n" + "\n\n".join(blocks)


# ----------------------------------------------------------------- L1 --

def render_l1(fit, l1_filled):
    required = fit.get("required")
    any_of = fit.get("any_of", [])
    all_ids = ([required] if required else []) + list(any_of)
    l1_filled = l1_filled if isinstance(l1_filled, dict) else {}

    table = ["| Column Name | Clay Native Action / Logic | Configuration |", "|---|---|---|"]
    blocks = []
    field_map = {}
    for i, cid in enumerate(all_ids, 1):
        info = l1_filled.get(cid, {})
        cost = info.get("cost", "search")
        inputs = info.get("inputs") or "{{CLAUDE: name the Clay columns this reads}}"
        body = block(info.get("body")) or "{{CLAUDE: write this fit condition's Claygent prompt}}"
        field = output_field("fit", cid)
        field_map[cid] = field
        name = title_case(cid) + (" (required)" if cid == required else "")
        config = info.get("summary") or first_sentence(info.get("body", "")) or \
            "{{CLAUDE: one-line configuration summary}}"

        table.append(f"| **{name}** | {ACTION_LABEL.get(cost, ACTION_LABEL['search'])} | {config} |")

        entry = (
            f"### 3.{i} — {name}\n"
            f"**Inputs:** {inputs}\n"
            f"**Only run if:** `Disqualified = false`\n"
            f"**Output:** TRUE / FALSE / UNKNOWN → `{field}`\n\n"
            f"```\n{body}\n```"
        )
        if info.get("note"):
            entry += f"\n\n> {clean(info['note'])}"
        blocks.append(entry)

    req_field = field_map.get(required)
    any_fields = [field_map[a] for a in any_of if a in field_map]
    lines = []
    if req_field:
        lines.append(f'  {req_field} = "TRUE",')
    if any_fields:
        lines.append("  OR(" + ", ".join(f'{f} = "TRUE"' for f in any_fields) + ")")
    combine_formula = "AND(\n" + "\n".join(lines) + "\n)"

    table.append("| **Fit** | `Formula` | Combines the required condition "
                  "with at least one supporting condition. |")
    blocks.append(
        f"### 3.{len(all_ids) + 1} — Fit\n"
        f"**Inputs:** all of the above\n"
        f"**Output:** boolean → `Fit`\n\n"
        f"```\n{combine_formula}\n```"
    )
    return "\n".join(table) + "\n\n" + "\n\n".join(blocks)


# ----------------------------------------------------------------- L2 --

def l2_action_label(signal):
    if signal.get("titles") or signal.get("terms"):
        return "`Find Jobs at Company`"
    return "`Google Search` + `AI Column`"


def l2_prompt(signal):
    lines = [
        f"Determine whether {{{{Company Name}}}} shows evidence of: "
        f"{clean(signal.get('note') or signal['type'].replace('_', ' '))}."
    ]
    if signal.get("implies"):
        lines.append(clean(signal["implies"]))
    if signal.get("terms"):
        lines.append("Look for these terms in job posts: " + ", ".join(signal["terms"]) + ".")
    if signal.get("titles"):
        t = "Titles: " + ", ".join(signal["titles"]) + "."
        if signal.get("excluded"):
            t += " Excluded (too universal to be causal): " + ", ".join(signal["excluded"]) + "."
        lines.append(t)
    if signal.get("stages"):
        lines.append("Stages: " + ", ".join(signal["stages"]) + ".")
    lb = signal.get("lookback_days", 90)
    lines.append(f"Lookback: last {lb} days only.")
    lines.append("Return TRUE, FALSE, or UNKNOWN, with the source URL and event date if TRUE.")
    return "\n".join(lines)


def l2_bullets(signal, field, show_tightness):
    bullets = []
    if show_tightness and signal.get("tightness"):
        bullets.append(f"Tightness: {signal['tightness']}")
    bullets.append(f"Lookback: {signal.get('lookback_days', 90)} days")
    if signal.get("implies"):
        bullets.append(f"Implies: {clean(signal['implies'])}")
    elif signal.get("note"):
        bullets.append(f"Note: {clean(signal['note'])}")
    if signal.get("terms"):
        bullets.append("Terms: " + ", ".join(signal["terms"]))
    if signal.get("titles"):
        t = "Titles: " + ", ".join(signal["titles"])
        if signal.get("excluded"):
            t += " (excluded: " + ", ".join(signal["excluded"]) + ")"
        bullets.append(t)
    if signal.get("stages"):
        bullets.append("Stages: " + ", ".join(signal["stages"]))
    bullets.append(f"Output: `{field}` → date + source URL, or null")
    return "\n".join(f"   - {b}" for b in bullets)


def render_l2_and_penalties(window, penalties):
    tier_fields = {"a": [], "b": [], "c": []}
    sections = []
    step_n = 1

    tier_meta = [
        ("tier_a", "A", "need ≥1 to qualify", True),
        ("tier_b", "B", "supporting", False),
        ("tier_c", "C", "context, never scores alone", False),
    ]
    for tier_key, label, desc, show_tightness in tier_meta:
        signals = window.get(tier_key, [])
        if not signals:
            continue
        items = []
        for i, s in enumerate(signals, 1):
            field = output_field("l2", s["type"])
            tier_fields[tier_key[-1]].append((field, s))
            items.append(
                f"{i}. **{s['type']}** — {l2_action_label(s)}\n"
                f"{l2_bullets(s, field, show_tightness)}\n\n"
                f"   ```\n{indent(l2_prompt(s))}\n   ```"
            )
        sections.append(f"### 4.{step_n} — Tier {label} signals ({desc})\n\n" + "\n\n".join(items))
        step_n += 1

    penalty_fields = []
    if penalties:
        items = []
        for i, p in enumerate(penalties, 1):
            field = f"penalty_{i}"
            penalty_fields.append((field, p))
            prompt = (
                f"Determine whether {{{{Company Name}}}} meets this condition: "
                f"{clean(p['trigger'])}\n"
                f"Lookback: last {p.get('lookback_months', 6)} months only.\n"
                f"Return TRUE, FALSE, or UNKNOWN, with the source URL and event date if TRUE."
            )
            bullets = "\n".join(f"   - {b}" for b in [
                f"Lookback: {p.get('lookback_months', 6)} months",
                f"Points: {p['points']}",
                f"Output: `{field}` → date + source URL, or null",
            ])
            items.append(
                f"{i}. **{field}** — `Google Search` + `AI Column`\n"
                f"{bullets}\n\n"
                f"   ```\n{indent(prompt)}\n   ```"
            )
        sections.append(f"### 4.{step_n} — Penalties\n\n" + "\n\n".join(items))

    return "\n\n".join(sections), tier_fields, penalty_fields


# ----------------------------------------------------------------- L3 --

def recency_expr(date_field, points, brackets):
    expr = "0"
    for b in reversed(brackets):
        expr = f"IF(DAYS_SINCE({date_field}) <= {b['max_days']}, {points} * {b['multiplier']}, {expr})"
    return expr


def recency_line(brackets):
    parts = []
    prev = 0
    for b in brackets:
        start = prev + 1 if prev else 0
        parts.append(f"{start}–{b['max_days']}d ×{b['multiplier']}")
        prev = b["max_days"]
    return " · ".join(parts)


def render_l3(spec, tier_fields, penalty_fields):
    sc = {**DEFAULTS, **(spec.get("scoring") or {})}
    brackets = sc["recency"]

    table = ["| Criterion | Field Evaluated | Scoring |", "|---|---|---|"]
    if tier_fields["a"]:
        table.append(f"| Tier A | {', '.join(f'`{f}`' for f, _ in tier_fields['a'])} | "
                      f"{sc['tier_a_points']} pts each, cap {sc['tier_a_cap']}, recency multiplier applies |")
    if tier_fields["b"]:
        table.append(f"| Tier B | {', '.join(f'`{f}`' for f, _ in tier_fields['b'])} | "
                      f"{sc['tier_b_points']} pts each, cap {sc['tier_b_cap']} |")
    if tier_fields["c"]:
        table.append(f"| Tier C | {', '.join(f'`{f}`' for f, _ in tier_fields['c'])} | "
                      f"{sc['tier_c_points']} pts each, cap {sc['tier_c_cap']} |")
    if penalty_fields:
        table.append(f"| Penalties | {', '.join(f'`{f}`' for f, _ in penalty_fields)} | "
                      f"{'; '.join(str(p['points']) + ' pts' for _, p in penalty_fields)} |")

    a_terms = [recency_expr(f"/{f}_date", sc["tier_a_points"], brackets) for f, _ in tier_fields["a"]]
    a_sum = " +\n  ".join(a_terms) if a_terms else "0"
    b_terms = [f'IF(/{f} = "TRUE", {sc["tier_b_points"]}, 0)' for f, _ in tier_fields["b"]]
    b_sum = " + ".join(b_terms) if b_terms else "0"
    c_terms = [f'IF(/{f} = "TRUE", {sc["tier_c_points"]}, 0)' for f, _ in tier_fields["c"]]
    c_sum = " + ".join(c_terms) if c_terms else "0"
    pen_terms = [f'IF(/{f} = "TRUE", {p["points"]}, 0)' for f, p in penalty_fields]
    pen_sum = " + ".join(pen_terms) if pen_terms else "0"
    count_terms = [f'IF(/{f} = "TRUE", 1, 0)' for f, _ in tier_fields["a"]]
    count_sum = " + ".join(count_terms) if count_terms else "0"

    formula = f"""tier_a_subtotal = MIN({sc['tier_a_cap']},
  {a_sum}
)

tier_b_subtotal = MIN({sc['tier_b_cap']}, {b_sum})

tier_c_subtotal = MIN({sc['tier_c_cap']}, {c_sum})

penalty_total = {pen_sum}

tier_a_count = {count_sum}

final_score = tier_a_subtotal + tier_b_subtotal + tier_c_subtotal + penalty_total

Qualified = AND(tier_a_count >= 1, final_score >= {sc['threshold']})"""

    inputs = ", ".join(f"/{f}" for f, _ in
                        tier_fields["a"] + tier_fields["b"] + tier_fields["c"]) or "l2_* columns"
    if penalty_fields:
        inputs += ", " + ", ".join(f"/{f}" for f, _ in penalty_fields)

    return (
        "\n".join(table) + "\n\n"
        f"Recency (Tier A only): {recency_line(brackets)}\n\n"
        f"**Gate:** `Qualified = AND(tier_a_count >= 1, final_score >= {sc['threshold']})`\n\n"
        "### 5.1 — Scoring Formula\n"
        f"**Inputs:** {inputs}\n"
        "**Only run if:** `AND(Disqualified = false, Fit = true)`\n"
        "**Output:** number → `final_score`; boolean → `Qualified`\n\n"
        f"```\n{formula}\n```"
    )


# ----------------------------------------------------------------- L4 --

def render_l4(tier_fields, penalty_fields):
    inputs = ", ".join(f"/{f}" for f, _ in
                        tier_fields["a"] + tier_fields["b"] + tier_fields["c"]) or "l2_* columns"
    if penalty_fields:
        inputs += ", " + ", ".join(f"/{f}" for f, _ in penalty_fields)
    body = """Extract every signal found for {{Company Name}} from the row data.

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
- Return [] if nothing qualifies."""
    table = ("| Column Name | Clay Native Action / Logic | Configuration |\n"
              "|---|---|---|\n"
              "| **Evidence Extraction** | `AI Column` (web search off) | "
              "Extracts every dated, sourced signal from the row into structured JSON. |")
    detail = (
        "### 6.1 — Evidence Extraction\n"
        f"**Inputs:** {inputs}\n"
        "**Only run if:** `Qualified = true`\n"
        "**Output:** JSON array → `l4_evidence`\n\n"
        f"```\n{body}\n```"
    )
    return table + "\n\n" + detail


# ----------------------------------------------------------------- L5 --

def render_l5(spec, marker):
    intake = spec.get("intake", {})
    context_fields = marker(
        "CONTEXT_FIELDS",
        "list the row fields worth passing — size, current vendors, fit evidence",
    )
    body = f"""You are evaluating whether {{{{Company Name}}}} is likely to buy
{spec['offer']} in the next {intake.get('window_length', '90 days')}.

Evidence: {{l4_evidence}}
Company context: {context_fields}

First decide: is there a genuine buying window?
Consider whether this company would source this externally at
all, whether they supply or self-serve it, and whether anyone
internally owns this decision yet.

If no: return exactly NO_WINDOW and one sentence why.

If yes: lead with the single strongest signal and its date,
then one sentence connecting it to {intake.get('demand_noun', 'demand for this offer')}. Cite only
what appears in the evidence. Do not assert need the evidence
does not support. Under 45 words."""
    table = ("| Column Name | Clay Native Action / Logic | Configuration |\n"
              "|---|---|---|\n"
              "| **Adjudication** | `AI Column` (web search off) | "
              "Evaluates whether a genuine buying window exists; can return `NO_WINDOW`. |")
    detail = (
        "### 7.1 — Adjudication\n"
        "**Inputs:** /l4_evidence, plus the row fields named in the prompt below\n"
        "**Only run if:** `Qualified = true`\n"
        "**Output:** text → `l5_rationale` (or exactly `NO_WINDOW`)\n\n"
        f"```\n{body}\n```"
    )
    return table + "\n\n" + detail


# ------------------------------------------------------------- shared --

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
    body = ["## Discovery — hand this to the client", ""]
    if qs:
        body += [f"{i}. {clean(q)}" for i, q in enumerate(qs, 1)]
    else:
        body.append("*(no discovery questions written — add them before handing this over)*")
    return "\n".join(body)


NOT_VERIFIED = {
    "corroborated": "Corroborated across multiple case studies — not confirmed against actual deal data.",
    "inferred": "Inferred from public evidence — not confirmed against actual deal data.",
    "assumed": "A placeholder assumption — needs direct client confirmation before this spec ships.",
}


def build_context(spec, marker):
    intake = spec.get("intake", {})
    conf = intake.get("hypothesis_confidence", "assumed")
    flag = {"inferred": " ⚠", "assumed": " ⚠"}.get(conf, "")
    not_verified = NOT_VERIFIED.get(conf)

    motion = clean(spec.get("motion", "")) or marker(
        "MOTION", "state which motion this spec targets, and why the size floor sits where it does")
    offer_type = intake.get("offer_type", "?")
    offer_type_reasoning = marker(
        "OFFER_TYPE_REASONING",
        "explain in a sentence or two why this offer is readiness or manufacturable, "
        "and which motion it serves if the offer splits across motions",
    )
    scope_exclusions = marker(
        "SCOPE_EXCLUSIONS",
        "list what this spec deliberately does not cover — other motions, segments, "
        "or checks left out, and why",
    )
    hyp = clean(intake.get("buying_event_hypothesis") or intake.get("buying_event"))
    evidence = clean(intake.get("hypothesis_evidence", ""))

    parts = [
        f"# {spec['client']} — build sequence",
        "## The offer",
        clean(spec["offer"]),
        "## The motion this spec targets",
        motion,
        "## Offer type",
        f"**{offer_type.capitalize()}.** {offer_type_reasoning}",
        "## Trigger hypothesis",
        f"> {hyp}\n\n**Confidence:** `{conf}`{flag}\n\n{evidence}" +
        (f"\n\n**Not yet verified:** {not_verified}" if not_verified else ""),
        "## What this spec does not do",
        scope_exclusions,
    ]
    return "\n\n".join(parts)


# --------------------------------------------------------------- main --

def compile_spec(spec, filled=None):
    filled = filled or {}
    unfilled = []

    def marker(key, prompt):
        if filled.get(key):
            return filled[key]
        unfilled.append(key)
        return "{{CLAUDE: " + prompt + "}}"

    sourcing = spec.get("sourcing", {})
    fit = spec.get("fit", {})
    window = spec.get("window", {})
    penalties = spec.get("penalty", [])

    l2_block, tier_fields, penalty_fields = render_l2_and_penalties(window, penalties)

    # unfilled tracking for L0/L1 hand-authored content
    l0_filled = filled.get("l0", {}) or {}
    l1_filled = filled.get("l1", {}) or {}
    for c in spec.get("disqualify", []):
        if not (l0_filled.get(c["id"], {}) or {}).get("body"):
            unfilled.append(f"l0.{c['id']}")
    for cid in ([fit.get("required")] if fit.get("required") else []) + list(fit.get("any_of", [])):
        if not (l1_filled.get(cid, {}) or {}).get("body"):
            unfilled.append(f"l1.{cid}")

    parts = [
        build_context(spec, marker),
        render_sourcing(sourcing),
        fill("L0-disqualification.md", {"L0_CONTENT": render_l0(spec.get("disqualify", []), l0_filled)}),
        fill("L1-fit.md", {"L1_CONTENT": render_l1(fit, l1_filled)}),
        fill("L2-window.md", {"L2_CONTENT": l2_block}),
        fill("L3-scoring.md", {"L3_CONTENT": render_l3(spec, tier_fields, penalty_fields)}),
        fill("L4-evidence.md", {"L4_CONTENT": render_l4(tier_fields, penalty_fields)}),
        fill("L5-adjudication.md", {"L5_CONTENT": render_l5(spec, marker)}),
        fill("step8-test.md", {"REGRESSION_TABLE": regression_table(spec.get("regression", []))}),
        fill("step9-ship.md", {}),
        discovery_section(spec),
    ]
    return "\n\n---\n\n".join(p.rstrip("\n") for p in parts), unfilled


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
