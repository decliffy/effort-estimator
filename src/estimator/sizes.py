from dataclasses import dataclass
from enum import Enum


class TShirtSize(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


@dataclass(frozen=True)
class SizeDefinition:
    size: TShirtSize
    effort_range: str
    description: str
    indicators: list[str]


SIZE_DEFINITIONS: list[SizeDefinition] = [
    SizeDefinition(
        size=TShirtSize.XS,
        effort_range="< half a day",
        description="Isolated change; well-understood; no design needed",
        indicators=["single file change", "no new abstractions", "< 50 lines affected"],
    ),
    SizeDefinition(
        size=TShirtSize.S,
        effort_range="half–1 day",
        description="Small, clear-scope change; minimal testing surface",
        indicators=["1–3 files", "no new dependencies", "straightforward logic"],
    ),
    SizeDefinition(
        size=TShirtSize.M,
        effort_range="2–3 days",
        description="Moderate complexity; some design required; standard test coverage",
        indicators=["multiple files", "some new logic", "integration with existing components"],
    ),
    SizeDefinition(
        size=TShirtSize.L,
        effort_range="1–2 weeks",
        description="Significant work; planning required; integration concerns",
        indicators=["cross-module changes", "new abstractions", "non-trivial testing"],
    ),
    SizeDefinition(
        size=TShirtSize.XL,
        effort_range="2–4 weeks",
        description="Complex feature; multiple components; possible cross-team coordination",
        indicators=["new subsystem", "API changes", "data model changes", "performance concerns"],
    ),
    SizeDefinition(
        size=TShirtSize.XXL,
        effort_range="> 1 month",
        description="Epic-level; MUST be decomposed before meaningful estimation",
        indicators=["multi-team effort", "architectural changes", "unknown unknowns", "break it down first"],
    ),
]
