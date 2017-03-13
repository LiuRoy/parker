# -*- coding: utf-8 -*-
"""获取没拍视频列表"""
import re
import os
import requests
from pyquery import PyQuery

from spider.tools.common import (
    WebVideo,
    get_md5,
    parse_task,
)
from spider.models.videos import Videos
from spider.config.conf import (
    params,
    logger,
    statsd_client,
)


def get_user_id(html):
    """从html中找到user_id

    Args:
        html (string): 页面
    Returns:
        string: 用户id
    """
    result = re.search(r"var suid = '(.+?)';", html)
    return result.group(1)


def get_video_lists(html, source, task_id):
    """从获取的视频数据中找到感兴趣的数据

    Args:
        html (string): 视频html页面数据
        source (string): 网站类型
        task_id (int): 任务id
    Returns:
        list<WebVideo> 视频信息列表
    """
    page = PyQuery(html)
    result = []
    for item in page("div[class='card_wrapping']"):
        title = item.xpath("./div[@class='h_title']")[0].text
        img_url = item.xpath("./a/div")[0].get("data-url")
        play_data = os.path.basename(img_url)
        video_url = 'http://www.miaopai.com/show/{}.htm'.format(
            play_data.split('_')[0])

        result.append(WebVideo(
            source=source,
            task_id=task_id,
            img_url=img_url,
            duration=0,
            title=title,
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
    source, task_id = parse_task(name)
    try:
        response = requests.get(url, timeout=10)
        if not response.ok:
            statsd_client.incr('miaopai.extract.exc')
            logger.error('request failure. url:{} name:{}'.format(url, name))
            return

        user_id = get_user_id(response.text)
        video_page_url = 'http://m.miaopai.com/show/getOwnerVideo?suid={}&page=1&per={}'.format(
            user_id, params['video_number_per_page'])
        response = requests.get(video_page_url, timeout=10)
        if not response.ok:
            statsd_client.incr('miaopai.extract.exc')
            logger.error('request failure. url:{} name:{}'.format(video_page_url, name))
            return

        video_div = response.json()['msg']
        videos = get_video_lists(video_div, source, task_id)
    except Exception as exc:
        statsd_client.incr('miaopai.extract.exc')
        logger.error('request failure. name:{}'.format(name))
        logger.exception(exc)
    else:
        statsd_client.incr('miaopai.extract.suc')
        logger.info('request success. name:{}'.format(name))
        new_videos = Videos.filter_exist(videos)
        Videos.batch_add(new_videos)
        return new_videos
