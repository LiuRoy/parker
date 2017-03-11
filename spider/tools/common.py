# -*- coding: utf-8 -*-
"""一些公用结构体"""
import hashlib
from collections import namedtuple


WebVideo = namedtuple(
    'WebVideo', [
        'source',           # string 网站类型
        'task_id',          # int    定时任务id
        'img_url',          # string 图片链接
        'duration',         # int    播放时长
        'title',            # string 视频标题
        'video_url',        # string 视频链接
        'video_url_md5',    # string 视频链接md值
    ])

VideoInfo = namedtuple(
    'VideoInfo', [
        'video_id',        # int Videos记录id
        'video_url',       # string 播放url
        'format',          # string 视频格式
        'container',       # string flv/mp4/avi
        'profile',         # string 1080P/高清/标清
        'size',            # int 视频大小
    ])


def parse_task(task_name):
    """解析定时任务名称获取任务类型和id

    Args:
        task_name (string): 任务名称
    Returns:
        source (string): 网站类型
        task_id int: 任务id
    """
    source, task_id = task_name.split('-')
    return source, int(task_id)


def parse_video_time(v_time):
    """解析视频时长

    Args:
        v_time (string): 视频时长 格式: 4:50:89 01:29
    Returns:
        int 视频时长秒数
    """
    items = v_time.split(':')
    if len(items) == 2:
        return int(items[0]) * 60 + int(items[1])

    if len(items) == 3:
        return int(items[0]) * 3600 + int(items[1]) * 60 + int(items[2])

    return 0


def get_md5(content):
    """计算md5

    Args:
        content (string): 要计算md5的字符串
    Returns:
        string: 计算好的md5值
    """
    md5 = hashlib.md5()
    md5.update(content.encode('utf-8'))
    return md5.hexdigest()
