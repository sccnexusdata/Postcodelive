from __future__ import annotations
from collections import Counter

def quality_report(items: list[dict]) -> dict:
    total=len(items); geocoded=sum(i.get("latitude") is not None and i.get("longitude") is not None for i in items)
    sourced=sum(bool(i.get("provenance")) for i in items); imaged=sum(bool(i.get("image_url")) for i in items)
    return {
      "total": total,
      "by_kind": dict(Counter(i.get("kind","unknown") for i in items)),
      "geocoded_coverage": round(geocoded/total,4) if total else 0,
      "provenance_coverage": round(sourced/total,4) if total else 0,
      "image_coverage": round(imaged/total,4) if total else 0,
    }
