from dataclasses import dataclass, field


@dataclass(frozen=True)
class Objective:
    objective_id: str
    description: str
    requested_by: str
    constraints: tuple[str, ...] = field(default_factory=tuple)
    consequential: bool = False
