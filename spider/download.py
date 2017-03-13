# -*- coding: utf-8 -*-
"""下载视频任务"""
from spider import app
from spider.tools.task import ParkerTask
from spider.pull.you_get import (
    get_video_info,
    download_video
)


@app.task(base=ParkerTask, bind=True)
def bilibili(self, video):
    """根据bilibili播放地址下载视频

    Args:
        video (Videos): 视频记录
    """
    video_info = get_video_info(video.video_url, video.task_id)
    download_video(video_info)


@app.task(base=ParkerTask, bind=True)
def miaopai(self, video):
    """根据miaopai播放地址下载视频

    Args:
        video (Videos): 视频记录
    """
    video_info = get_video_info(video.video_url, video.task_id)
    download_video(video_info)
