# routed-memory

Implementation test of [Routed Continual Learning](https://arxiv.org/abs/2610.38796)
(Meta FAIR): route incoming memories into clusters instead of growing one flat
pool, then retrieve only from the relevant cluster. The paper reports similar
answer quality at a large fraction of the retrieval cost.

## Use case

A personal assistant that remembers facts and preferences across sessions.
This benchmark simulates exactly that: 10 facts about one user collected over
time (work stack, allergies, gym routine, city, agency, travels, university,
family health, messaging style, invoicing), then one recall query per fact.

## First offline result (token-Jaccard similarity, no embeddings)

```
memories: 10, clusters: 4
retrieval_accuracy: 60%
avg items scanned routed: 2.6  vs  flat pool: 10
context cost reduction: 74%
```

60% accuracy with token overlap only; the remaining misses are the mechanism's
known weak spot (queries that share no vocabulary with the target fact), which
is what embeddings are for in a real deployment. The 74% context saving is the
claim under test, and it holds offline.

## Use it

```python
from routedmemory import MemoryItem, MemoryClusters

mc = MemoryClusters(routing_threshold=0.18, max_clusters=4)
mc.route(MemoryItem("m1", "user prefers TypeScript for frontend"))
mc.route(MemoryItem("m2", "user is allergic to fish and lentils"))

result = mc.retrieve("what foods must be excluded?")
for item in result.found:
    print(item.text)
print(f"scanned {result.scanned} of {result.full_pool_size} memories")
```

```bash
python3 -m pytest tests/   # offline, zero dependencies
```

## Real deployment notes

- Swap token Jaccard for embedding cosine (local model, e.g. a small GGUF
  embedder) — routing logic and benchmark stay identical
- With an LLM in the loop, retrieval accuracy is what matters; scanned-item
  count is the API cost proxy the paper optimizes
- Memory stays on disk, per cluster: a GDPR-friendly layout (each cluster is
  a deletable group)

## Next steps

- Embedding backend (local GGUF embedder) behind the same interface
- Forgetting policy per cluster (TTL, dedupe)
- Benchmark against a flat pool with a real LLM judge instead of substring
  matching

## Citation

Independent implementation test. Cite the paper first:
arXiv:2610.38796 (Routed Continual Learning).

MIT
