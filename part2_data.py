from __future__ import annotations
from typing import Optional
import math

TREE_START_MOVE = -math.inf


class RecommendationTree:
    """Recommendation Tree class.

    Instance Attributes:
        - move: the current move which represents the standard deviation (move is -math.inf at the start)

    Representation Invariants:
        - (self.move is None) == (self._left_subtree is None)
        - (self.move is None) == (self._right_subtree is None)
    """
    move: Optional[float]

    # Private Instance Attributes:
    #   - _left_subtree:

    _left_subtree: Optional[RecommendationTree]
    _right_subtree: Optional[RecommendationTree]

    def __init__(self, move: Optional[float] = TREE_START_MOVE) -> None:
        """Initialize a new RecommendationTree containing only the given move value.

        Initialize an empty RecommendationTree
        """
        self.move = None
        self._left_subtree = None
        self._right_subtree = None

    def is_empty(self) -> bool:
        """Return whether this RecommendationTree is empty.
        """
        return self.move is None
