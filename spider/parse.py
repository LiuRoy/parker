# -*- coding: utf-8 -*-
"""解析页面任务"""

from spider import app
from spider.extract import (
    youku
)


@app.task
def youku(url, name):
    """抓取优酷页面 解析获取最新视频地址

    Args:
        url (string): 优酷页面地址
        name (string): 定时任务名称
    """
    videos = youku.extract_list_page(url, name)
    if videos:
        pass
        # todo 异步调用下载


@app.task
def bilibili(url, name):
    """抓取哔哩哔哩页面 解析获取最新视频地址

    Args:
        url (string): 哔哩哔哩页面地址
        name (string): 定时任务名称
    """
    pass
