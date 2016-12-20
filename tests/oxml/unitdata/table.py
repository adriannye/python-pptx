# encoding: utf-8

"""
Test data for table-related unit tests.
"""

from __future__ import absolute_import

from ...unitdata import BaseBuilder


class CT_TableCellBuilder(BaseBuilder):
    __tag__ = 'a:tc'
    __nspfxs__ = ('a',)
    __attrs__ = (
        'gridSpan', 'hMerge'
    )

class CT_TableCellPropertiesBuilder(BaseBuilder):
    __tag__ = 'a:tcPr'
    __nspfxs__ = ('a',)
    __attrs__ = (
        'marL', 'marR', 'marT', 'marB', 'vert', 'anchor', 'anchorCtr',
        'horzOverflow'
    )


def a_tc():
    return CT_TableCellBuilder()

def a_tcPr():
    return CT_TableCellPropertiesBuilder()
