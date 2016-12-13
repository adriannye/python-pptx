# encoding: utf-8

"""
Category-related objects. The |Categories| object is returned by
``Plot.categories`` and contains zero or more |Category| objects, each
representing one of the category labels associated with the plot. Categories
can be hierarchical, so there are members allowing discovery of the depth of
that hierarchy and means to navigate it.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from collections import Sequence


class Categories(Sequence):
    """
    A sequence of |Category| objects, each representing a category label on
    the chart. Provides properties for dealing with hierarchical categories.
    """
    def __init__(self, xChart):
        super(Categories, self).__init__()
        self._xChart = xChart

    def __getitem__(self, idx):
        pt = self._xChart.cat_pts[idx]
        return Category(pt, idx)

    def __len__(self):
        # a category can be "null", meaning the Excel cell for it is empty.
        # In this case, there is no c:pt element for it. The "empty" category
        # will, however, be accounted for in c:cat//c:ptCount/@val, which
        # reflects the true length of the categories collection.
        return self._xChart.cat_pt_count

    @property
    def depth(self):
        """
        Return an integer representing the number of hierarchical levels in
        this category collection. Returns 1 for non-hierarchical categories
        and 0 if no categories are present (generally meaning no series are
        present).
        """
        cat = self._xChart.cat
        if cat is None:
            return 0
        if cat.multiLvlStrRef is None:
            return 1
        return len(cat.lvls)


class Category(str):
    """
    An extension of `str` that provides the category label as its string
    value, and additional attributes representing other aspects of the
    category.
    """
    def __new__(cls, pt, *args):
        category_label = '' if pt is None else pt.v.text
        return str.__new__(cls, category_label)

    def __init__(self, pt, idx=None):
        """
        *idx* is a required attribute of a c:pt element, but must be
        specified when pt is None, as when a "placeholder" category is
        created to represent a missing c:pt element.
        """
        self._element = self._pt = pt
        self._idx = idx
