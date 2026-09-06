# Domain research protocol

What to search, in what order, and what each source can and cannot tell
you. Use when you have a domain and no client access.

## 1. The offer itself

**Look at:** homepage, product pages, pricing, docs, changelog.

**Establishes:** what they sell, to whom, price band, whether it's
self-serve or sales-led, technical depth.

**Price band matters more than it looks.** Self-serve under $100/mo means
no procurement, no champion, and a window measured in days — usually too
short to detect. Sales-led with "contact us" pricing means a buying
committee and a window measured in months. That single fact tells you
whether a build is viable.

## 2. Competitors and substitutes

**Look at:** their comparison pages, G2/Capterra category pages,
"alternatives to X" content.

**Establishes:** the substitute list, which becomes the penalty column.

**Also ask what people do instead of buying anything.** For Ramp it's a
corporate Amex and a spreadsheet. The status-quo substitute is usually
the real competitor and rarely appears on comparison pages.

## 3. Who supplies this category

**Establishes:** L0 competing supply.

Ask directly: **could a prospect in this market be a supplier rather than
a buyer?** For inference compute, yes — Docker, Modal, Baseten, the
hyperscalers. For corporate cards, yes — every fintech.

This is the check that catches the most embarrassing false positives,
because suppliers look like perfect fits on every activity signal.

## 4. What locks a company out

**Look at:** cloud provider partner pages, vendor case studies, press
releases announcing partnerships, 10-Ks if public.

**Establishes:** L0 lock-in.

A published multi-year partnership or co-selling agreement is strong
evidence the account will not switch on the strength of a few job posts.
This is the check BlackLine taught us — public since 2019, and missed
because nothing was looking for it.

## 5. Case studies — the highest-value source

**Look at:** their customer stories, in volume. Read five or more.

**Establishes:** the closest public proxy for the buying event.

Case studies conventionally open with the customer's situation before
buying. That "before" paragraph is the trigger, filtered through
marketing. Read several and look for **what repeats**. A situation
appearing in five out of eight stories is a real pattern.

**What this can't give you:** timing. A case study says a company was
struggling with manual reconciliation. It does not say the CFO started
six weeks earlier. Case studies establish the *condition*; you still have
to infer the *event* that created it.

## 6. Their own outbound and content

**Look at:** LinkedIn posts from their AEs and founders, webinar topics,
what their content marketing argues.

**Establishes:** what they believe triggers a purchase.

If their content keeps hammering one problem, their sales team hears
about that problem constantly. That's cheap signal about the trigger.

## 7. Job posts — theirs

**Look at:** their own careers page.

**Establishes:** motion, not trigger. Heavy AE hiring means sales-led and
volume-hungry, which means they want a wide list. A single enterprise AE
means they want twenty perfect accounts. This changes the threshold you
set, not the signals you pick.

---

## Confidence ladder

Label every spec field with where it came from:

| Level | Meaning |
|---|---|
| `verified` | stated directly on their site or in filings |
| `corroborated` | repeats across three or more independent sources |
| `inferred` | reasoned from category logic, no direct evidence |
| `assumed` | placeholder, needs client confirmation |

**L0 and L1 should be `verified` or `corroborated`.** If a disqualifier
is `inferred`, it is likely too aggressive — soften it or drop it, since
a wrong disqualifier silently deletes good accounts and you will never
see what you lost.

**L2 Tier A will usually be `inferred`.** That is expected and it is why
the Discovery section exists. Say so rather than dressing it up.

## The tightness test for Tier A

For each candidate signal, complete this sentence:

> "A company does X only when Y is happening."

- **Tight** — "A company posts a job naming vLLM only when it is serving
  models in production."
- **Medium** — "A company hires a Controller only when finance process
  needs an owner." Mostly true, with exceptions.
- **Loose** — "A company raises a Series B only when it needs [thing]."
  False. Money goes anywhere.

If the sentence needs heavy qualification, the signal is Tier B or C.
Tier A is reserved for links that hold without hedging.
