from dataclasses import dataclass, field
from estimator.sizes import TShirtSize

_MAX_DESCRIPTION_LENGTH = 4000


@dataclass
class EstimationRequest:
    description: str
    truncated: bool = field(init=False, default=False)

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise ValueError("Task description must not be empty.")
        if len(self.description) > _MAX_DESCRIPTION_LENGTH:
            self.description = self.description[:_MAX_DESCRIPTION_LENGTH]
            self.truncated = True


@dataclass
class EstimationResult:
    request: EstimationRequest
    size: TShirtSize
    rationale: str
    assumptions: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.rationale or not self.rationale.strip():
            raise ValueError("rationale must not be empty.")
        if not isinstance(self.size, TShirtSize):
            raise ValueError(f"size must be a TShirtSize enum value, got {type(self.size)}")


@dataclass
class EstimationError:
    request: EstimationRequest
    message: str

    def __post_init__(self):
        if not self.message or not self.message.strip():
            raise ValueError("message must not be empty.")


@dataclass
class BatchEstimationRequest:
    tasks: list[EstimationRequest]

    def __post_init__(self):
        if not self.tasks:
            raise ValueError("Batch must contain at least one task.")


@dataclass
class BatchEstimationResult:
    results: list
