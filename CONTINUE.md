# CONTINUE.md — read this first when an agent picks up this repo

## What this repo is

Implementation test of *Routed Continual Learning* (arXiv:2610.38796, Meta
FAIR): route incoming memories into clusters instead of one flat pool,
retrieve only from the relevant cluster. Use case: a personal assistant that
remembers facts across sessions. Offline bench: 10 facts, 4 clusters, 60%
retrieval accuracy with token Jaccard, 74% context-cost reduction vs a flat
pool. Honest status: mechanism check with lexical similarity — **not** a
reproduction of the paper's numbers.

## Working rules

- **Offline-first**: `python -m unittest` from the repo root must stay green
  with zero dependencies. The embedding backend (ROADMAP item 1) must stay
  optional and lazy — never a hard import.
- **Honest claims**: the 60%/74% numbers are a token-Jaccard mechanism check
  on 10 synthetic facts, never a benchmark result. Say so everywhere.
- Independent implementation — cite the paper first, never imply affiliation
  with the authors. Commits: English, conventional style.
- Before pushing: run `python -m unittest`; it must be green.

## Models — Z.ai Coding Plan (only if an LLM judge is added)

- base: `https://api.z.ai/api/coding/paas/v4`
- model: `glm-5.3-flash` ONLY
- Flat subscription. On a billing/quota/endpoint error: **STOP and report** —
  never switch providers or models. Owner-approval-gated.

## Current task (do this now)

Nothing in progress. Start with ROADMAP item 1 (embedding backend) — pick a
small local GGUF embedder, keep it optional, keep the bench interface
unchanged. Item 3's LLM-judge part is money-gated: propose, wait for the
owner's OK.

## STOP points

- Any billing/auth/endpoint error → stop, report, wait.
- If an embedder changes routing behavior, report old-vs-new bench numbers in
  the same commit — never swap similarity silently.
