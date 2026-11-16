# ROADMAP — routed-memory

Ordered by value. Nothing here needs money; all items stay offline unless
marked.

## 1. Embedding backend behind the same interface

Swap token-Jaccard for embedding cosine with a small local GGUF embedder.
`MemoryClusters(routing_threshold=...)` and the benchmark stay identical;
only the similarity function changes. The known weak spot (queries sharing no
vocabulary with the target fact) is exactly what this fixes.

## 2. Forgetting policy per cluster

TTL + dedupe inside each cluster. Deletion granularity is already
cluster-shaped, which is the GDPR-friendly layout the README promises —
make the policy explicit and testable.

## 3. Stronger benchmark

- Recall queries that share no tokens with the fact (the 40% miss class).
- A real LLM judge instead of substring matching (money-gated: Z.ai Coding
  Plan, `glm-5.3-flash` only, owner approval first).
- Scale beyond 10 facts: 50–100, multiple clusters saturating `max_clusters`.

## 4. Compare against flat pool with the same embedder

Once item 1 lands, re-run the bench flat-vs-routed with identical retrieval
so the cost-reduction number is apples-to-apples with real vectors.

## Done

- v0.1.0 — cluster routing + routed retrieval + 10-fact offline bench
  (60% accuracy, 74% context-cost reduction with token Jaccard), 4 offline
  tests, CI on Linux/Windows/macOS.
