# encoding: utf-8

"""
Unit test suite for the pptx.chart.category module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from pptx.chart.category import Categories, Category, CategoryLevel

from ..unitutil.cxml import element
from ..unitutil.mock import call, class_mock, instance_mock


class DescribeCategories(object):

    def it_knows_its_length(self, len_fixture):
        categories, expected_len = len_fixture
        assert len(categories) == expected_len

    def it_supports_indexed_access(self, getitem_fixture):
        categories, idx, Category_, pt, category_ = getitem_fixture
        category = categories[idx]
        Category_.assert_called_once_with(pt, idx)
        assert category is category_

    def it_knows_its_depth(self, depth_fixture):
        categories, expected_value = depth_fixture
        assert categories.depth == expected_value

    def it_provides_access_to_its_levels(self, levels_fixture):
        categories, CategoryLevel_, calls, expected_levels = levels_fixture
        levels = categories.levels
        assert CategoryLevel_.call_args_list == calls
        assert levels == expected_levels

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('c:barChart',                                                  0),
        ('c:barChart/c:ser/c:cat',                                      1),
        ('c:barChart/c:ser/c:cat/c:multiLvlStrRef/c:lvl',               1),
        ('c:barChart/c:ser/c:cat/c:multiLvlStrRef/(c:lvl,c:lvl)',       2),
        ('c:barChart/c:ser/c:cat/c:multiLvlStrRef/(c:lvl,c:lvl,c:lvl)', 3),
    ])
    def depth_fixture(self, request):
        xChart_cxml, expected_value = request.param
        categories = Categories(element(xChart_cxml))
        return categories, expected_value

    @pytest.fixture(params=[
        ('c:barChart/c:ser/c:cat/(c:ptCount{val=2})',             0, None),
        ('c:barChart/c:ser/c:cat/(c:ptCount{val=2},c:pt{idx=1})', 0, None),
        ('c:barChart/c:ser/c:cat/(c:ptCount{val=2},c:pt{idx=1})', 1, 0),
        ('c:barChart/c:ser/c:cat/c:lvl/(c:ptCount{val=2},c:pt{idx=1})',
         1, 0),
    ])
    def getitem_fixture(self, request, Category_, category_):
        xChart_cxml, idx, pt_offset = request.param
        xChart = element(xChart_cxml)
        pt = None if pt_offset is None else xChart.xpath('.//c:pt')[pt_offset]
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

    @pytest.fixture(params=[
        ('c:barChart',                                                  0),
        ('c:barChart/c:ser/c:cat',                                      0),
        ('c:barChart/c:ser/c:cat/c:multiLvlStrRef/c:lvl',               1),
        ('c:barChart/c:ser/c:cat/c:multiLvlStrRef/(c:lvl,c:lvl)',       2),
        ('c:barChart/c:ser/c:cat/c:multiLvlStrRef/(c:lvl,c:lvl,c:lvl)', 3),
    ])
    def levels_fixture(self, request, CategoryLevel_, category_level_):
        xChart_cxml, level_count = request.param
        xChart = element(xChart_cxml)
        lvls = xChart.xpath('.//c:lvl')
        categories = Categories(xChart)
        calls = [call(lvl) for lvl in lvls]
        expected_levels = [category_level_ for _ in range(level_count)]
        return categories, CategoryLevel_, calls, expected_levels

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Category_(self, request, category_):
        return class_mock(
            request, 'pptx.chart.category.Category', return_value=category_
        )

    @pytest.fixture
    def category_(self, request):
        return instance_mock(request, Category)

    @pytest.fixture
    def CategoryLevel_(self, request, category_level_):
        return class_mock(
            request, 'pptx.chart.category.CategoryLevel',
            return_value=category_level_
        )

    @pytest.fixture
    def category_level_(self, request):
        return instance_mock(request, CategoryLevel)


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


class DescribeCategoryLevel(object):

    def it_knows_its_length(self, len_fixture):
        category_level, expected_len = len_fixture
        assert len(category_level) == expected_len

    def it_supports_indexed_access(self, getitem_fixture):
        category_level, idx, Category_, pt, category_ = getitem_fixture
        category = category_level[idx]
        Category_.assert_called_once_with(pt)
        assert category is category_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[0, 1, 2])
    def getitem_fixture(self, request, Category_, category_):
        idx = request.param
        lvl_cxml = 'c:lvl/(c:pt,c:pt,c:pt)'
        lvl = element(lvl_cxml)
        pt = lvl.xpath('./c:pt')[idx]
        category_level = CategoryLevel(lvl)
        return category_level, idx, Category_, pt, category_

    @pytest.fixture(params=[
        ('c:lvl',                  0),
        ('c:lvl/c:pt',             1),
        ('c:lvl/(c:pt,c:pt)',      2),
        ('c:lvl/(c:pt,c:pt,c:pt)', 3),
    ])
    def len_fixture(self, request):
        lvl_cxml, expected_len = request.param
        category_level = CategoryLevel(element(lvl_cxml))
        return category_level, expected_len

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Category_(self, request, category_):
        return class_mock(
            request, 'pptx.chart.category.Category', return_value=category_
        )

    @pytest.fixture
    def category_(self, request):
        return instance_mock(request, Category)
