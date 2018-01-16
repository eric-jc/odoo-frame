# coding: utf-8


class ReportColumn(object):
    # fm = '<td style="border-bottom: 1px solid gray;border-top:none;">a</td>'
    # _style_top_default = 'border-top:none;'
    # _style_bottom_default = 'border-bottom: 1px solid gray;'

    def __init__(self, value='', column_info=None):
        self._value = value
        self._column_info = column_info

    def add_value(self, value):
        self._value = value if value else u''

    def add_column_info(self, column_info):
        self._column_info = column_info

    def get(self):
        fm = u'<td{0}>{1}</td>'
        style = u' style="border-top:none;"'
        if self._column_info:
            style = str(self._column_info)
        return fm.format(style, self._value)
