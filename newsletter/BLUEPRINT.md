# Blueprint — a weekly letter for the DULSS study group

**Status:** design draft v0.1
**Owner:** study group (Chiradip Mandal, Craig Rodrigues)
**Sources of the spine:** `dulss-book-rev2` (Vol 1 preface; Vol 2 plan), `dulss-vol1-labs`
(§1 "reading isn't owning"), this repo's `definition.md` and Guiding Principles.

---

## 1. The one-sentence thesis

> **Every issue takes one guarantee, states it as a machine-checkable invariant, prices it in
> physics, and hands the reader the derivation and the lab that make it theirs.**

That is the entire product. It is Vol 2's spine (*correctness and speed are the same problem
viewed from two sides*) and this repo's definition (*safety and liveness as a design contract*)
compressed into a weekly artifact.

## 2. Positioning — why this is not ByteByteGo

ByteByteGo optimizes for **recall at breadth**: a diagram, a vocabulary, an interview answer. It
is a good product for a different reader. This letter optimizes for **ownership at depth**: after
reading, you can re-derive the result on a whiteboard and defend the number under attack.

| | The breadth letter | This letter |
|---|---|---|
| Unit of content | A system, surveyed | A guarantee, priced |
| Reader leaves with | A diagram to recognize | A derivation to reconstruct |
| Claim style | "How X works" | "X holds iff …; here is where it breaks" |
| Proof burden | Cite the paper | State the theorem, show the steps |
| Failure mode we accept | Small audience | — |
| Failure mode we refuse | — | Content that flatters the reader |
| Success metric | Subscribers | Counterexamples, PRs, graded labs |

**Target audience** (deliberately narrow): staff/principal engineers who have felt a system fail
at scale and want the theory made precise, and graduate researchers who have met the algorithms in
isolation. Same two audiences as the Vol 1 preface. A ceiling of ~2,000 *right* readers is a
success, not a compromise.

## 3. Non-negotiable quality bars

Inherited verbatim from the study group's Guiding Principles, applied to prose:

1. **No product pitches.** A vendor's system may be the subject; never the point.
2. **First principles or nothing.** If it cannot be derived, measured, or model-checked, it does
   not ship.
3. **Verifiable claims.** Theorem, spec, benchmark harness, or code path — attached, not alluded to.
4. **Transferable.** The lesson must survive the example being replaced.

**Standing refusals** (the list is the brand): top-N lists, X-vs-Y verdicts, career advice, tool
announcements, LLM-adjacent hype, "system design interview" framing, and any issue whose claim
cannot be falsified.

## 4. Issue skeleton — fixed, ~1,400 words, 7 minutes

The fixed shape is what makes it small and high-impact: the reader knows exactly where the proof
starts and can enter at their own altitude.

| Block | Budget | Content |
|---|---|---|
| **1. The Claim** | 60 w | One falsifiable sentence, above the fold. No preamble, no throat-clearing. |
| **2. The Cost** | 250 w | What the guarantee physically costs: a log flush, a round trip, a latch hold, a clock-uncertainty wait. |
| **3. The Derivation** | 500 w | The theorem or the measurement, complete. One figure, produced from a script in-repo. |
| **4. The Engineering** | 350 w | How a real system buys the guarantee back cheaply. Named code path or paper section. |
| **5. The Assignment** | 150 w | A 15-minute derivation or a `make grade`-able lab in `dulss-vol1-labs`. Answer next issue. |
| **6. Errata & counterexamples** | 100 w | Reader corrections, attributed. Our own errors first. |

One issue = one claim. If a second claim appears, it is next week's issue.

## 5. The flywheel (why a small letter compounds here)

```
book chapter ──► newsletter issue ──► study-group session ──► lab / exercise
     ▲                                                              │
     └────────────────── errata & reader counterexamples ◄──────────┘
```

The letter is the **funnel into the session** and the **errata engine for the book**. Vol 1's
editorial handoff already found a wrong MTTF formula, a false range-locality bound, and Raft's
Figure-8 pitfall taught in its unsafe form. Publishing weekly, with readers hunting, industrializes
that discovery — and each catch becomes an exercise no future reader can get wrong.

## 6. Cadence — a 4-week cycle anchored to the monthly session

| Week | Issue type | Ties to |
|---|---|---|
| 1 | **Pre-read** — the coming session's paper made legible; the two questions to hold in mind | Luma event, Discord |
| 2 | **Derivation** — the theorem under that paper, proved | Book chapter |
| 3 | **Debrief** — the hard questions the room actually asked, and what survived them | Session recording |
| 4 | **Build** — a lab; autograder ships with the issue | `dulss-vol1-labs` |

Ship Thursday. A missed week is published as a missed week, not backfilled with filler.

## 7. Mechanics

- **Archive is this repo.** One `newsletter/NNN/index.md` per issue, GitHub Pages as the canonical
  archive, mailer (Buttondown/Listmonk) as transport. Same pattern as `001/`, `002/`.
- **The archive accepts pull requests.** A reader who finds an error fixes it and is credited in
  the commit. No newsletter platform can offer this; it is the single most distinctive mechanic
  available to us, and it is free because we already live in git.
- **Every figure and number is reproducible**: the script that made it sits beside the issue.
- **Cross-linking**: each issue names the chapter it derives from and the lab it feeds.

## 8. Metrics — and the one we refuse

Track: replies containing a derivation, PRs against the archive, lab submissions, issue→session
attendance conversion, counterexamples published.
Do not track or optimize: subscriber count, open rate, share count. Growth is a by-product of being
the only letter that proves things.

## 9. Recurring segment concepts (each ≤ 25 words)

1. **The Invariant** — One guarantee per issue, written as a machine-checkable predicate, then priced in flushes, round trips, and latch holds.
2. **Prove It in Ten Lines** — A theorem the field quotes but rarely proves, compressed to ten steps a reader can reconstruct from memory.
3. **The Wrong Number** — Recompute a famous figure — eleven nines, hedging's collapse, tail amplification — until the assumption that breaks it is visible.
4. **Falsify This** — We publish a claim we believe. Readers attack it. Next issue prints the best counterexample, with the author's name.
5. **Spec of the Week** — Sixty lines of TLA+ for one protocol rule; the model checker finds the bug you would have shipped.
6. **Paper vs. Production** — One paper's guarantee, one deployed code path, and the exact line where the implementation stops matching the proof.
7. **The Post-Mortem Theorem** — A real outage traced to the invariant it violated, stated formally. Incidents treated as existence proofs, not stories.
8. **Errata as Content** — An error in our own book, published with the exercise that would have caught it. Reading isn't owning.
9. **One Benchmark, Honestly** — A single measurement with its full setup, its confidence interval, and an explicit list of claims it does not support.
10. **The Decision Table** — A design space collapsed to conditions and costs, no verdict. The reader chooses, then defends the choice.
11. **Read This Instead** — One paragraph on why the famous paper on a topic is the wrong entry point, and which obscure one is right.
12. **The Assignment** — A war story converted into a graded lab; the autograder ships with the issue, solutions the week after.

## 10. Candidate names (each ≤ 25 words)

- ***The Load-Bearing Result*** — every issue carries one result the rest of the field stands on, and shows it holding weight.
- ***Guarantee & Cost*** — the Vol 2 spine as a masthead: name the promise, then name what it costs in physics.
- ***Invariant*** — one word, weekly, machine-checkable; matches the study group's definition of an engineered ultra-large-scale system.
- ***The Expedition*** — from the series pitch: if the survey books are the map of the territory, this is the expedition.
- ***Bounded Surface*** — from `definition.md`: bounded capability surface, unbounded capacity. Signals the audience in two words and repels everyone else.

## 11. First six issues (a concrete run, each ≤ 25 words)

1. **What a quorum actually buys.** Derive `R + W > N` from intersection, then show the three deployments where it silently stops protecting you.
2. **Eleven nines, recomputed.** The durability claim everyone quotes, rebuilt from independent-failure assumptions, then broken by correlated failure. The honest number is smaller.
3. **Raft's Figure 8, taught safely.** The commit rule most tutorials get wrong, the execution that exposes it, and the TLA+ spec that catches it.
4. **fsync lied to you.** The WAL invariant, the storage stack that violates it, and how to test your own disk in twenty minutes.
5. **Write skew passes every test.** Snapshot isolation's exact gap from serializability, as a dependency graph, with the smallest example that separates them.
6. **Hedged requests and the p^r collapse.** Why tail-latency hedging looks miraculous, and the independence assumption that makes it fail in production.

---

## 12. Open decisions

- **Name** — pick from §10 before issue 001.
- **Transport** — Buttondown (markdown-native, cheap) vs. Listmonk (self-hosted, owns the list).
- **Author rotation** — single voice vs. rotating with session presenters. Recommend single voice
  for the first ten issues to fix the register, then invite.
- **Length discipline** — enforce the §4 budget by word count in CI, or by editorial judgment.
