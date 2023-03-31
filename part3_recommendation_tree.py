"""CSC111 Winter 2023 Phase 2: Decoding the Secrets of Successful Stocks (Part 2)

Instructions (READ THIS FIRST!)
===============================

...

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of our group
memebers at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please consult Yehyun Lee at yehyun.lee@mail.utoronto.ca.

This file is Copyright (c) 2023 Yehyun Lee, Aung Zwe Maw and Wonjae Lee.
"""

from __future__ import annotations
from typing import Optional
import part2_factor_data_processing
from lxml import etree  # This is only used for except statement. This is auto imported by pandas.
from urllib.error import HTTPError  # Same case


class RecommendationTree:
    """Recommendation Tree class.

    Instance Attributes:
        - factor: the factor for this current Recommendation Tree
        - correlation: the correlation for this current Recommendation Tree

    Representation Invariants:
        - If self.factor is None, then all other Instance Attributes are None.
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

    # Private Instance Attributes:
    #   - _left_subtree:
    #       The left subtree, or None if this tree is empty
    #   - _right_subtree:
    #       The right subtree, or None if this tree is empty

    _left_subtree: Optional[RecommendationTree]
    _right_subtree: Optional[RecommendationTree]
    _list_of_stocks: Optional[list]

    def __init__(self, factor: Optional[str], correlation: Optional[float] = 0) -> None:
        """Initialize a new RecommendationTree containing only the given move value.

        Initialize an empty RecommendationTree if self.factor is None
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
            self._left_subtree = RecommendationTree(None, None)  # self._left_subtree is an empty RecommendationTree
            self._right_subtree = RecommendationTree(None, None)  # self._right_subtree is an empty RecommendationTree
            self._list_of_stocks = []

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

    def __str__(self) -> str:
        """Return a string representation of this tree.
        # >>> c = create_game_tree([('f3', 1), ('f2', 2), ('f1', 3], 2)
        # >>> print(c) str(c)
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
        string = ' ' * depth + f'{self.factor}: {", ".join(self._list_of_stocks)}\n'
        if self._left_subtree.factor is not None:
            string += self._left_subtree._str_indented(depth + 2)
        if self._right_subtree.factor is not None:
            string += self._right_subtree._str_indented(depth + 2)
        return string

    def add_subtree(self, left_or_right: str, subtree: RecommendationTree) -> None:  # update correlaton value
        """Add subtree to this RecommendationTree's left or right subtree."""
        if left_or_right == 'left':
            self._left_subtree = subtree
        else:
            self._right_subtree = subtree

    def move_stock_to_subtree(self, stock: tuple[str, dict[str, float]]):
        """
        Use stock corrrelation factor value to compare with
        """
        # stock[0] is the stock name
        # 1 compare correlation
        # 2 determine where to go, left or right
        # 3 go into that subtree and recall this method
        # 4 stop at leaf
        # 5 append stock name to list_of_stocks
        if self._left_subtree.factor is None and self._right_subtree.factor is None:
            self._list_of_stocks.append(stock[0])
        else:
            if stock[1][self.factor] <= self.correlation:
                self._left_subtree.move_stock_to_subtree(stock)
            else:
                self._right_subtree.move_stock_to_subtree(stock)

    def get_leaf_recommendation_tree(self) -> list[RecommendationTree]:
        """  This function would be used to run through the recommendation tree
        that has already stocks that are classified and will return the recommendation tree
        that is a leaf in order from left to right
        """
        if self._left_subtree.factor is None and self._right_subtree.factor is None:
            return [self]
        else:
            leaf_nodes = []
            if self._left_subtree is not None:
                leaf_nodes.extend(self._left_subtree.get_leaf_recommendation_tree())
            if self._right_subtree is not None:
                leaf_nodes.extend(self._right_subtree.get_leaf_recommendation_tree())
            return leaf_nodes

    def ranked_choices_of_stocks(self) -> dict[int, list[str]]:
        """ This ranks the stocks from the leaf nodes from right to left
        as a dictionary starting with the key of 1.
        Preconditions:
        """
        leafs = self.get_leaf_recommendation_tree()
        leafs_with_stock = [leaf._list_of_stocks for leaf in leafs]
        return {i+1: leaf for i, leaf in enumerate(leafs_with_stock)}

    def insert_stocks(self, stocks: list[str], end_date: str, factors: list[str]) -> None:
        """
        Insert multiple stocks into
        Preconditions:
        - stocks != []
        - end_date
        - self.is_empty() is not None
        - end-date != ''
        """
        for stock in stocks:  # Classify each stock into game_tree
            try:
                self.move_stock_to_subtree(
                    (stock, part2_factor_data_processing.all_factors_correlation(stock, end_date, factors)))
            except (etree.XMLSyntaxError, HTTPError):
                continue


# [tree._list_of_stocks for tree in recommendation_tree.get_leaf_recommendation_tree() if tree._list_of_stocks != []]


def create_recommendation_tree(factors_correlation: list[tuple[str, float]], d: int) -> RecommendationTree:
    """
    Create a complete recommendation tree of depth d.

    For the returned Recommendation Tree:
        - If d == 0, a size-one RecommendationTree is returned.

    Preconditions:
        - factors_correlation is sorted (smallest to highest)
        - factors_correlation != []
        - d >= 0
    """
    root_factor, root_correlation = factors_correlation[d]
    recommendation_tree = RecommendationTree(root_factor, root_correlation)
    if d == 0:  # Base Case
        return recommendation_tree
    else:
        left_subtree = create_recommendation_tree(factors_correlation, d - 1)   # Recursion Step
        right_subtree = create_recommendation_tree(factors_correlation, d - 1)
        recommendation_tree.add_subtree('left', left_subtree)   # Add to subtree
        recommendation_tree.add_subtree('right', right_subtree)
        return recommendation_tree


def determining_buy_stocks(recommendation_tree: RecommendationTree, risk_percentage: int) -> list[str]:
    """
    Returns a list of stocks that chooses which stocks to buy.

    <risk_percentage> defintion and usage:
        - <risk_percentage> is converted into an int -> (len(ranked_choices) * risk_percentage) // 100
        - Based on the number from <risk_percentage> that is converted to int, we choose which stocks to buy from the
            far right of <recommendation_tree>.
        - For example, if the converted <risk_percentage> is 1, then the far right is chosen.
        - Another example: if the converted <risk_percentage> is 2, then the two of the furthest right is chosen.
        - After the chosen stocks are determined, the rest of the stocks is not bought.

    Preconditions:
        - 1 <= risk_percentage <= 100
    """
    ranked_choices = recommendation_tree.ranked_choices_of_stocks()
    range_of_buy_leafs = len(ranked_choices) - ((len(ranked_choices) * risk_percentage) // 100)
    # Drop empty list and pick ranked list of stocks based on percentage risk
    nested_buy_stocks = [ranked_choices[choices] for choices in ranked_choices if
                         choices > range_of_buy_leafs and ranked_choices[choices] != []]
    buy_stocks = [item for sublist in nested_buy_stocks for item in sublist]  # Converts nested list to flat list
    return buy_stocks


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod(verbose=True)
#
#     import python_ta
#     python_ta.check_all(config={
#         'extra-imports': [part2_factor_data_processing],  # the names (strs) of imported modules
#         'allowed-io': [],  # the names (strs) of functions that call print/open/input
#         'max-line-length': 120
#     })
