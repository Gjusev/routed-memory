"""Data types."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MemoryItem:
    id: str
    text: str
    cluster: str = ""


@dataclass
class ClusterStats:
    name: str
    items: int = 0


@dataclass
class RetrievalResult:
    found: list[MemoryItem] = field(default_factory=list)
    # how many items a router-free retrieval would have scanned
    full_pool_size: int = 0
    # how many items the routed retrieval actually considered
    scanned: int = 0
