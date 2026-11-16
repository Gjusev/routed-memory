"""Offline tests for the routing mechanism.

Plain unittest so they run with `python -m unittest` -- no pytest, no
dependencies (see README).
"""

import unittest

from routedmemory import MemoryItem, MemoryClusters, run_bench


class TestRouting(unittest.TestCase):
    def test_routing_creates_clusters_by_topic(self):
        mc = MemoryClusters()
        items = [
            MemoryItem("1", "user works out at the gym four times a week"),
            MemoryItem("2", "user does cardio at the gym on weekends"),
            MemoryItem("3", "user invoices clients in EUR currency"),
        ]
        mc.route(items[0])
        mc.route(items[1])
        mc.route(items[2])
        # gym items should share a cluster, invoicing should not
        self.assertEqual(items[0].cluster, items[1].cluster)
        self.assertNotEqual(items[2].cluster, items[0].cluster)

    def test_retrieval_scans_less_than_full_pool(self):
        mc = MemoryClusters()
        texts = [
            "user prefers TypeScript for frontend",
            "user is allergic to fish and lentils",
            "user trains at the gym daily",
            "user lives in Kreuztal near Siegen",
            "user runs the Mokka digital agency",
            "user travelled to Barcelona last year",
            "user studies at FOM university",
        ]
        for i, t in enumerate(texts):
            mc.route(MemoryItem(f"m{i}", t))
        result = mc.retrieve("where does the user live?")
        self.assertEqual(result.full_pool_size, 7)
        self.assertLess(result.scanned, result.full_pool_size)  # the routed saving

    def test_benchmark_reports_savings_with_good_accuracy(self):
        report = run_bench()
        self.assertGreaterEqual(report["retrieval_accuracy"], 0.5)  # mechanism retrieves most facts
        self.assertGreater(report["context_cost_reduction"], 0)     # routed scan beats full pool
        self.assertGreater(report["clusters"], 1)
        self.assertLessEqual(report["clusters"], 4)

    def test_threshold_extremes(self):
        # threshold 0: everything lands in one cluster, no saving
        flat = run_bench(routing_threshold=0.0, max_clusters=1)
        self.assertEqual(flat["clusters"], 1)
        self.assertEqual(flat["context_cost_reduction"], 0.0)


if __name__ == "__main__":
    unittest.main()
