from __future__ import annotations
from typing import Optional
import math

TREE_START_CORR = -math.inf


class RecommendationTree:
    """Recommendation Tree class.

    Instance Attributes:
        - move: the current move which represents the correlation (move is -math.inf at the start)
        - investment: the amount of capital that the decision tree has


    Representation Invariants:
        - (self.move is None) == (self._left_subtree is None)
        - (self.move is None) == (self._right_subtree is None)
    """

    # corr value float
    # factor name str ex) 'pe-ratio'
    # links = ['pe-ratio', 'price-sales', 'price-book', 'roe', 'roa', 'return-on-tangible-equity',
    #          'number-of-employees', 'current-ratio', 'quick-ratio', 'total-liabilities',
    #          'debt-equity-ratio', 'roi', 'cash-on-hand', 'total-share-holder-equity', 'revenue', 'gross-profit',
    #          'net-income', 'shares-outstanding', 'stock-price-history']
    # subtrees
    factor: Optional[str]
    correlation: Optional[float]
    _left_subtree: Optional[RecommendationTree]
    _right_subtree: Optional[RecommendationTree]
    _list_of_stocks: Optional[list]

    def __init__(self, factor: Optional[str], correlation: Optional[float] = TREE_START_CORR) -> None:
        """Initialize a new RecommendationTree containing only the given move value.

        Initialize an empty RecommendationTree
        """
        if factor is None:
            self.factor = None
            self.correlation = None
            self._left_subtree = None
            self._right_subtree = None
            self._list_of_stocks = None
        else:
            self.factor = factor
            self.correlation = correlation
            self._left_subtree = RecommendationTree(None, None)  # self._left_subtree is an empty BST
            self._right_subtree = RecommendationTree(None, None)  # self._right_subtree is an empty RecommendationTree
            self._list_of_stocks = []

    def is_empty(self) -> bool:
        """Return whether this RecommendationTree is empty.
        """
        # if self.factor is None and self.correlation is None:
        #     return True
        # else:
        #     return False
        return self.factor is None and self.correlation is None

    def get_subtrees(self) -> list[RecommendationTree] | None:
        """Return the subtrees of this recommendation tree."""
        # return list(self._left_subtree)

    # def find_subtree_by_move(self, move: str | tuple[str, ...]) -> Optional[RecommendationTree]:
    #     """Return the subtree corresponding to the given move.
    #
    #     Return None if no subtree corresponds to that move.
    #     """
    #     if move in self._left_subtree:
    #         return self._left_subtree.move
    #     elif move in self._right_subtree:
    #         return self._right_subtree.move
    #     else:
    #         return None

    def __len__(self) -> int:
        """Return the number of items in this tree."""

    def __str__(self) -> str:
        """Return a string representation of this tree.
        # >>> c = create_game_tree([('f3', 1), ('f2', 2), ('f1', 3], 2)
        # >>> print(c)
        # f1: 1
        #   f2: 2
        #     f3: 3
        #     f3: 3
        #   f2: 2
        #     f3: 3
        #     f3: 3
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.factor is None:
            return ''
        else:
            return (' ' * depth + f'{self.factor}: {self.correlation}\n' + self._left_subtree._str_indented(depth + 2)
                    + self._left_subtree._str_indented(depth + 2))

    def add_subtree(self, subtree: RecommendationTree) -> None:  # update correlaton value
        """Add a subtree to this game tree."""
        self._left_subtree = subtree
        self._right_subtree = subtree

    def move_stock_to_subtree(self, stock: tuple[str, dict[str, float]]):
        ...
        # 1 compare correlation
        # 2 determine where to go, left or right
        # 3 go into that subtree and recall this method
        # 4 stop at leaf
        if self._right_subtree is None and self._left_subtree is None:
            self._list_of_stocks.append(stock[0])
        else:
            if stock[1][self.factor] <= self.correlation:
                self._left_subtree.move_stock_to_subtree(stock)
            else:
                self._right_subtree.move_stock_to_subtree(stock)


# self.get_ordered_leaf
# self.get_subtree_by_move

def create_recommendation_tree(factors_correlation: list[tuple[str, float]], d: int) -> RecommendationTree:
    """ This function would create the full recommendation tree
    Preconditions:
    - #factors correlation is sorted
    - #d is not 0
    """
    root_factor, root_correlation = factors_correlation[d]
    recommendation_tree = RecommendationTree(root_factor, root_correlation)
    if d == 0:
        return recommendation_tree
    else:
        subtree = create_recommendation_tree(factors_correlation, d - 1)
        recommendation_tree.add_subtree(subtree)
        return recommendation_tree

# def create_simulation() ->


# def get_recommendation(companies: list[str])
