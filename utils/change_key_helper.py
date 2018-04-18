# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError


class ChangeKeyHelper(object):
    def __init__(self):
        self.invalid_keys = []
        self.index = 0
        self.change_key_dic = {}
        return

    def add_invalid_keys(self, keys):
        if not keys:
            return
        self.invalid_keys += keys
        return

    def add_key(self, key):
        if key in self.invalid_keys:
            raise ValidationError(u'使用了非法名称：' + key)
        new_key = self._get_new_key()
        self.change_key_dic[key] = new_key
        self.invalid_keys.append(new_key)
        return

    def get_new_key(self, key):
        if key in self.invalid_keys:
            raise ValidationError(u'使用了非法名称：' + key)
        new_key = self._get_new_key()
        self.change_key_dic[key] = new_key
        self.invalid_keys.append(new_key)
        return new_key

    def safe_get_key(self, key):
        if key in self.change_key_dic:
            return self.change_key_dic[key]
        return ''

    def _get_new_key(self):
        self.index += 1
        return 'param_' + str(self.index)
