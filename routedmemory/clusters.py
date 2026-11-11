"""Clustered memory: route new items to an existing cluster or start a new one.

Offline similarity = token Jaccard (no embeddings needed to test the routing
mechanism). A real deployment swaps this for embedding cosine; the routing
logic and the benchmark stay identical.
"""

from __future__ import annotations

import re

from .types import ClusterStats, MemoryItem, RetrievalResult

NEW_CLUSTER = "NEW"


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"\w+", text.lower()))


class MemoryClusters:
    def __init__(self, routing_threshold: float = 0.18, max_clusters: int = 8) -> None:
        # below this similarity an item opens a new cluster instead of joining
        self.routing_threshold = routing_threshold
        self.max_clusters = max_clusters
        self.clusters: dict[str, list[MemoryItem]] = {}

    def route(self, item: MemoryItem) -> str:
        """Return the cluster the item belongs to, creating one if needed."""
        best, best_score = None, 0.0
        target = _tokens(item.text)
        for name, members in self.clusters.items():
            if not members:
                continue
            centroid = _tokens(" ".join(m.text for m in members))
            union = target | centroid
            score = len(target & centroid) / len(union) if union else 0.0
            if score > best_score:
                best, best_score = name, score
        if best is not None and (best_score >= self.routing_threshold or len(self.clusters) >= self.max_clusters):
            self.clusters[best].append(item)
            item.cluster = best
            return best
        name = f"cluster_{len(self.clusters) + 1}"
        self.clusters[name] = [item]
        item.cluster = name
        return name

    def retrieve(self, query: str, max_items: int = 5) -> RetrievalResult:
        """Scan only the most similar cluster (the paper's cost saving)."""
        target = _tokens(query)
        best, best_score = None, 0.0
        for name, members in self.clusters.items():
            centroid = _tokens(" ".join(m.text for m in members))
            union = target | centroid
            score = len(target & centroid) / len(union) if union else 0.0
            if score > best_score:
                best, best_score = name, score
        pool = [it for members in self.clusters.values() for it in members]
        result = RetrievalResult(full_pool_size=len(pool))
        if best is None:
            return result
        members = self.clusters[best]
        result.scanned = len(members)
        scored = []
        for m in members:
            inter = len(target & _tokens(m.text))
            scored.append((inter, m))
        scored.sort(key=lambda pair: -pair[0])
        result.found = [m for _, m in scored[:max_items]]
        return result

    def stats(self) -> list[ClusterStats]:
        return [ClusterStats(name=n, items=len(m)) for n, m in self.clusters.items()]
