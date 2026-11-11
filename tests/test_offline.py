"""Offline tests for the routing mechanism."""

from routedmemory import MemoryItem, MemoryClusters, run_bench


def test_routing_creates_clusters_by_topic():
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
    assert items[0].cluster == items[1].cluster
    assert items[2].cluster != items[0].cluster


def test_retrieval_scans_less_than_full_pool():
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
    assert result.full_pool_size == 7
    assert result.scanned < result.full_pool_size  # the routed saving


def test_benchmark_reports_savings_with_good_accuracy():
    report = run_bench()
    assert report["retrieval_accuracy"] >= 0.5  # mechanism retrieves most facts
    assert report["context_cost_reduction"] > 0  # routed scan beats full pool
    assert 1 < report["clusters"] <= 4


def test_threshold_extremes():
    # threshold 0: everything lands in one cluster, no saving
    flat = run_bench(routing_threshold=0.0, max_clusters=1)
    assert flat["clusters"] == 1
    assert flat["context_cost_reduction"] == 0.0
