# -*- coding: utf-8 -*-
"""下载视频任务"""
from spider import app


@app.task
def bilibili(video):
    """根据优酷播放地址下载视频

    Args:
        video (Videos): 视频记录
    """
    pass
