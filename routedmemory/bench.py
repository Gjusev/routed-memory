"""Benchmark: routed retrieval vs full-pool retrieval.

Scenario (the use case): an assistant collects facts about its user over
sessions (work, food, travel, health, family). Each session ends with a query
that must recall one specific fact. We measure:

- accuracy: was the target fact among the retrieved items?
- context cost: how many memory items ended up in the prompt (routed scan vs
  the whole pool a flat memory would have to send)
"""

from __future__ import annotations

from .clusters import MemoryClusters
from .types import MemoryItem

# (memory text, query, expected substring in a retrieved item)
DEFAULT_SCENARIO = [
    ("User prefers working with TypeScript and Tailwind for frontend projects", "which stack does he like for frontend?", "TypeScript"),
    ("User is allergic to fish and lentils, exclude them from meal plans", "what foods must be excluded from recipes?", "lentils"),
    ("User trains at the gym four times a week and targets 180g protein daily", "how often does he work out?", "gym"),
    ("User lives in Kreuztal near Siegen in North Rhine-Westphalia", "where does the user live?", "Kreuztal"),
    ("User runs a digital agency called Mokka Agentur offering web development", "what is the name of his agency?", "Mokka"),
    ("User's favourite travel destination last year was Barcelona", "which city did he travel to last year?", "Barcelona"),
    ("User studies business informatics at FOM university alongside work", "which university does he attend?", "FOM"),
    ("User's mother lives in Germany and has a diagnosed lymphedema", "what health condition runs in the family?", "lymphedema"),
    ("User prefers Telegram voice messages over long text replies", "which messaging style does the user prefer?", "Telegram"),
    ("User invoices clients in EUR with 14-day payment terms", "what currency does he invoice in?", "EUR"),
]


class MemoryBench:
    def __init__(self, scenario: list[tuple[str, str, str]] | None = None,
                 routing_threshold: float = 0.18, max_clusters: int = 4) -> None:
        self.scenario = scenario or DEFAULT_SCENARIO
        self.clusters = MemoryClusters(routing_threshold=routing_threshold,
                                       max_clusters=max_clusters)

    def run(self) -> dict:
        # phase 1: collect memories across sessions
        for i, (text, _, _) in enumerate(self.scenario):
            self.clusters.route(MemoryItem(id=f"m{i}", text=text))

        # phase 2: recall queries
        hits, scanned_list, pool_size = 0, [], 0
        for i, (_, query, expected) in enumerate(self.scenario):
            result = self.clusters.retrieve(query, max_items=3)
            pool_size = max(pool_size, result.full_pool_size)
            scanned_list.append(result.scanned)
            if any(expected.lower() in it.text.lower() for it in result.found):
                hits += 1

        avg_scanned = sum(scanned_list) / len(scanned_list) if scanned_list else 0
        saving = 1 - (avg_scanned / pool_size) if pool_size else 0.0
        return {
            "memories": len(self.scenario),
            "clusters": len(self.clusters.clusters),
            "retrieval_accuracy": hits / len(self.scenario),
            "pool_size": pool_size,
            "avg_items_scanned_routed": round(avg_scanned, 2),
            "avg_items_scanned_flat": pool_size,
            "context_cost_reduction": round(saving, 4),
        }


def run_bench(scenario=None, routing_threshold: float = 0.18,
              max_clusters: int = 4) -> dict:
    bench = MemoryBench(scenario, routing_threshold, max_clusters)
    return bench.run()
