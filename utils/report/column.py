# coding: utf-8


class ReportColumn(object):
    # fm = '<td style="border-bottom: 1px solid gray;border-top:none;">a</td>'
    _style_top_default = 'border-top:none;'
    _style_bottom_default = 'border-bottom: 1px solid gray;'

    def __init__(self):
        self._style_top = ''
        self._style_bottom = ''
        self._style = ''
        self._value = ''
        self._column_info = None

    def add_style_border_bottom(self, _border_bottom=None):
        if _border_bottom and not _border_bottom.endswith(';'):
            _border_bottom += ';'
        self._style_bottom = _border_bottom or self._style_bottom_default

    def add_style_border_top(self, _border_top=None):
        if _border_top and not _border_top.endswith(';'):
            _border_top += ';'
        self._style_top = _border_top or self._style_top_default

    def add_style(self, _style):
        if _style and not _style.endswith(';'):
            _style += ';'
        self._style = self._style + _style if self._style else _style

    def add_value(self, value):
        self._value = value if value else ''

    def add_column_info(self, column_info):
        self._column_info = column_info

    def get(self):
        fm = '<td{0}>{1}</td>'
        style = ''
        if self._style_top or self._style_bottom or self._style:
            style = ' style="{}"'.format(self._style_top + self._style_bottom + self._style)
        if self._column_info:
            style = str(self._column_info)
        return fm.format(style, self._value)
