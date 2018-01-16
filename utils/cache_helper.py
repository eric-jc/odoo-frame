# -*- coding: utf-8 -*-


class CacheHelper(object):
    def __init__(self, env):
        self.dic = {}
        self.env = env

    def safe_get(self, key, value_if_empty=u'-无-'):
        if not key:
            return value_if_empty
        if key not in self.dic:
            result = self.env.search_read([('id', '=', key)], ['name'], limit=1)
            name = result[0]['name'] if result else u'-已删除-'
            self.dic[key] = name
        return self.dic[key]
