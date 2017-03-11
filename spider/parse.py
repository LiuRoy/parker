# -*- coding: utf-8 -*-
"""解析页面任务"""
from spider import app


@app.task
def bilibili(url, name):
    """抓取哔哩哔哩 解析获取最新视频地址

    Args:
        url (string): 哔哩哔哩页面地址
        name (string): 定时任务名称
    """
    pass


@app.task
def meipai(url, name):
    """抓取美拍页面 解析获取最新视频地址

    Args:
        url (string): 美拍页面地址
        name (string): 定时任务名称
    """
    pass
