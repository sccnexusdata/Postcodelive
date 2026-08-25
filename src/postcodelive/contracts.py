from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class Provenance:
    source: str
    source_type: str = "unknown"
    url: str | None = None
    observed_at: str | None = None
    confidence: str = "unreviewed"

@dataclass
class LocalityItem:
    id: str
    kind: str
    name: str
    category: str = "Uncategorised"
    latitude: float | None = None
    longitude: float | None = None
    postcode: str | None = None
    url: str | None = None
    image_url: str | None = None
    start: str | None = None
    end: str | None = None
    description: str | None = None
    provenance: list[dict[str, Any]] | None = None
    source_payload: dict[str, Any] | None = None

    def public_dict(self) -> dict[str, Any]:
        return {k:v for k,v in asdict(self).items() if v not in (None, [], {}, "") and k != "source_payload"}
