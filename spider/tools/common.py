# -*- coding: utf-8 -*-
"""一些公用结构体"""
from collections import namedtuple
import requests
from requests.exceptions import RequestException

from spider.config.conf import (
    statsd_client,
    logger,
)


VideoInfo = namedtuple(
    'VideoInfo', [
        'publisher',        # string 发布人名称
        'source',           # string 网站类型
        'task_id',          # int    定时任务id
        'comment_count',    # int    评论个数
        'star_count',       # int    点赞个数
        'play_count',       # int    播放次数
        'img_url',          # string 图片链接
        'duration',         # int    播放时长
        'title',            # string 视频标题
        'publish_date',     # int    发布日期
        'video_url'         # string 视频链接
    ])

VideoFormat = namedtuple(
    'VideoFormat', [
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


def http_get(url, headers=None, timeout=None):
    """HTTP GET方式获取页面

    Args:
        url (string): 链接
        headers (dict): 请求头
        timeout (float): 超时时间
    Returns:
        content (string): 页面内容
    """
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.ok:
            logger.info('request url success. url: {}'.format(url))
            statsd_client.incr('request.get.suc')
            return response.content
        else:
            logger.warning('request url warning. url: {}'.format(url))
            statsd_client.incr('request.get.warn')
    except RequestException as e:
        logger.error('request url failure. url: {}'.format(url))
        logger.exception(e)
        statsd_client.incr('request.get.exc')
