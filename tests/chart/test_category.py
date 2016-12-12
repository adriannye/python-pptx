# encoding: utf-8

"""
Unit test suite for the pptx.chart.category module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from pptx.chart.category import Categories, Category

from ..unitutil.cxml import element
from ..unitutil.mock import class_mock, instance_mock


class DescribeCategories(object):

    def it_knows_its_length(self, len_fixture):
        categories, expected_len = len_fixture
        assert len(categories) == expected_len

    def it_supports_indexed_access(self, getitem_fixture):
        categories, idx, Category_, pt, category_ = getitem_fixture
        category = categories[idx]
        Category_.assert_called_once_with(pt, idx)
        assert category is category_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('c:barChart/c:ser/c:cat/(c:ptCount{val=2},c:pt{idx=1})', 1, 0),
        # ('c:barChart/c:ser/c:cat/(c:ptCount{val=2},c:pt{idx=1}/c:v"Foo", 1)',
    ])
    def getitem_fixture(self, request, Category_, category_):
        xChart_cxml, idx, pt_offset = request.param
        xChart = element(xChart_cxml)
        pt = xChart.xpath('.//c:pt')[pt_offset]
        categories = Categories(xChart)
        return categories, idx, Category_, pt, category_

    @pytest.fixture(params=[
        ('c:barChart', 0),
        ('c:barChart/c:ser/c:cat/c:ptCount{val=4}', 4),
    ])
    def len_fixture(self, request):
        xChart_cxml, expected_len = request.param
        categories = Categories(element(xChart_cxml))
        return categories, expected_len

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Category_(self, request, category_):
        return class_mock(
            request, 'pptx.chart.category.Category', return_value=category_
        )

    @pytest.fixture
    def category_(self, request):
        return instance_mock(request, Category)


class DescribeCategory(object):

    def it_extends_str(self, base_class_fixture):
        category, str_value = base_class_fixture
        assert isinstance(category, str)
        assert category == str_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (None,            ''),
        ('c:pt/c:v"Foo"', 'Foo'),
    ])
    def base_class_fixture(self, request):
        pt_cxml, str_value = request.param
        pt = None if pt_cxml is None else element(pt_cxml)
        category = Category(pt)
        return category, str_value
