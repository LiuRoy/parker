# -*- coding: utf-8 -*-
"""解析页面任务"""
from spider import app
from spider import download
from spider.tools.task import ParkerTask
from spider import extract


@app.task(base=ParkerTask)
def bilibili(url, name):
    """抓取哔哩哔哩 解析获取最新视频地址

    Args:
        url (string): 哔哩哔哩页面地址
        name (string): 定时任务名称
    """
    new_videos = extract.bilibili.extract_videos(url, name)
    if new_videos:
        for video in new_videos:
            download.bilibili.delay(video)


@app.task(base=ParkerTask)
def miaopai(url, name):
    """抓取秒拍页面 解析获取最新视频地址

    Args:
        url (string): 美拍页面地址
        name (string): 定时任务名称
    """
    new_videos = extract.miaopai.extract_videos(url, name)
    if new_videos:
        for video in new_videos:
            download.miaopai.delay(video)
