from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass(frozen=True)
class LocalityConfig:
    slug: str; display_name: str; country: str; postcode_prefixes: tuple[str,...]
    latitude: float; longitude: float; radius_km: float; timezone: str = "Europe/London"

    @classmethod
    def load(cls, path: str|Path) -> "LocalityConfig":
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls(
            slug=raw["slug"], display_name=raw["display_name"], country=raw.get("country","GB"),
            postcode_prefixes=tuple(raw.get("postcode_prefixes", [])),
            latitude=float(raw["centre"]["latitude"]), longitude=float(raw["centre"]["longitude"]),
            radius_km=float(raw.get("radius_km", 16.0934)), timezone=raw.get("timezone","Europe/London")
        )
