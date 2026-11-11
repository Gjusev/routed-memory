"""routedmemory: implementation test of Routed Continual Learning (arXiv:2610.38796).

The paper: instead of one growing memory pool (retrieval cost grows with every
fact), route incoming memories into a small number of clusters and retrieve
only from the relevant cluster(s). Claim: similar answer quality at a fraction
of the retrieval cost.

Use case built in: a personal assistant that remembers preferences and facts
across sessions. Memory stays local (fits a GDPR-sensitive setup); the metric
is retrieval accuracy vs "context tokens" (items placed in the prompt).
"""

from .types import MemoryItem, ClusterStats
from .clusters import MemoryClusters
from .bench import MemoryBench, run_bench

__version__ = "0.1.0"
__all__ = ["MemoryItem", "ClusterStats", "MemoryClusters", "MemoryBench", "run_bench"]
