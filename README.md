# routed-memory

[![tests](https://github.com/Gjusev/routed-memory/actions/workflows/tests.yml/badge.svg)](https://github.com/Gjusev/routed-memory/actions/workflows/tests.yml)
[![dependencies](https://img.shields.io/badge/dependencies-0-success)]()
[![python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

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
python -m unittest   # offline, zero dependencies, runs on Linux/macOS/Windows
```

## Real deployment notes

- Swap token Jaccard for embedding cosine (local model, e.g. a small GGUF
  embedder) — routing logic and benchmark stay identical
- With an LLM in the loop, retrieval accuracy is what matters; scanned-item
  count is the API cost proxy the paper optimizes
- Memory stays on disk, per cluster: a GDPR-friendly layout (each cluster is
  a deletable group)

## Next steps

See [ROADMAP.md](ROADMAP.md) — next up: an embedding backend (local GGUF
embedder) behind the same interface, a forgetting policy per cluster, and a
stronger benchmark. [CONTINUE.md](CONTINUE.md) has the handoff rules for
coding agents picking this up.

## Repository layout

```
routedmemory/   MemoryItem, MemoryClusters, routing + retrieval, offline bench
tests/          offline unit tests (python -m unittest, zero dependencies)
ROADMAP.md      ordered next steps
CONTINUE.md     agent handoff: working rules + STOP points
```

## Citation

Independent implementation test. Cite the paper first:
arXiv:2610.38796 (Routed Continual Learning).

MIT
