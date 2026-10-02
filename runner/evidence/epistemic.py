from enum import Enum


class EpistemicState(str, Enum):
    UNKNOWN = "UNKNOWN"
    HYPOTHESIS = "HYPOTHESIS"
    INFERRED = "INFERRED"
    OBSERVED = "OBSERVED"
    VERIFIED = "VERIFIED"
    REPLICATED = "REPLICATED"
    QUALIFIED = "QUALIFIED"


def can_advance(current: EpistemicState, proposed: EpistemicState) -> bool:
    order = list(EpistemicState)
    return order.index(proposed) >= order.index(current)
