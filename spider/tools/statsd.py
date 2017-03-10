# -*- coding: utf-8 -*-
"""假监控客户端"""


class FakeStatsdClient(object):
    """假客户端"""
    def __init__(self, *args, **kwargs):
        pass

    def incr(self, *args, **kwargs):
        pass
