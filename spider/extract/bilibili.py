# -*- coding: utf-8 -*-
"""解析bilibili页面"""
import re
import requests
from spider.tools.common import (
    WebVideo,
    get_md5,
    parse_task,
    parse_video_time,
)
from spider.models.videos import Videos
from spider.config.conf import (
    params,
    logger,
    statsd_client,
)


def get_user_id(url):
    """从个人视频页链接解析出用户id

    Args:
        url (string): 人视频页链接
    Returns：
        int: 用户id
    """
    result = re.search(r'\d+', url)
    return int(result.group())


def get_video_lists(video_data, source, task_id):
    """从获取的视频数据中找到感兴趣的数据

    Args:
        video_data (dict): 视频数据
        source (string): 网站类型
        task_id (int): 任务id
    Returns:
        list<WebVideo> 视频信息列表
    """
    result = []
    for item in video_data['data']['vlist']:
        v_time = item['length']
        video_url = 'http://www.bilibili.com/video/av{}/'.format(item['aid'])

        result.append(WebVideo(
            source=source,
            task_id=task_id,
            img_url=item['pic'],
            duration=parse_video_time(v_time),
            title=item['title'],
            video_url=video_url,
            video_url_md5=get_md5(video_url)
        ))
    return result


def extract_videos(url, name):
    """解析视频列表

    Args:
        url (string): 哔哩哔哩页面地址
        name (string): 定时任务名称
    """
    user_id = get_user_id(url)
    source, task_id = parse_task(name)

    request_url = 'http://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&' \
                  'pagesize={}&tid=0&page=1&keyword=&order=senddate'.format(
        user_id, params['video_number_per_page'])
    try:
        response = requests.get(request_url, timeout=10)
        if not response.ok:
            statsd_client.incr('bilibili.extract.exc')
            logger.error('request failure. url:{} name:{}'.format(request_url, name))
            return

        video_data = response.json()
        videos = get_video_lists(video_data, source, task_id)
    except Exception as exc:
        statsd_client.incr('bilibili.extract.exc')
        logger.error('request failure. url:{} name:{}'.format(request_url, name))
        logger.exception(exc)
    else:
        statsd_client.incr('bilibili.extract.suc')
        logger.info('request success. url:{} name:{}'.format(request_url, name))
        new_videos = Videos.filter_exist(videos)
        return Videos.batch_add(new_videos)
