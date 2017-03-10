# -*- coding: utf-8 -*-
"""解析优酷页面"""
from pyquery import PyQuery
from spider.tools.common import (
    VideoInfo,
    parse_task,
    http_get
)
from spider.models.videos import Videos
from spider.config.conf import (
    logger,
    statsd_client,
)


def parse_count(count):
    """解析页面的展示个数

    Args:
        count (string): 页面展示的次数信息, 格式: 100 1,000 1.78万
    Returns:
        int
    """
    if count.isdigit():
        return int(count)

    if '万' in count:
        return int(10000 * float(count.replace('万', '')))

    if ',' in count:
        return int(count.replace(',', ''))

    return 0


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


def pars_list_page(page, source, task_id):
    """解析视频列表页面

    Args:
        page (string): html页面
        source (string): 网站类型
        task_id (int): 任务id
    Returns:
        list<VideoInfo> 视频信息列表
    """
    html = PyQuery(page)
    result = []
    for item in html("div[class='v']"):
        img_url = item.xpath("./div[@class='v-thumb']/img")[0].get('src')
        v_time = item.xpath("./div[@class='v-thumb']/div/span")[0].text

        link_element = item.xpath("./div[@class='v-link']/a")[0]
        video_url = link_element.get('href')
        video_title = link_element.get('title')

        entry_elements = item.xpath("./div[@class='v-meta va']/div[@class='v-meta-entry']/span")
        play_count = entry_elements[0].text
        comment_count = entry_elements[1].text

        result.append(VideoInfo(
            publisher=None,
            source=source,
            task_id=task_id,
            comment_count=parse_count(comment_count),
            star_count=None,
            play_count=parse_count(play_count),
            img_url=img_url.strip(),
            duration=parse_video_time(v_time),
            title=video_title.strip(),
            publish_date=None,
            video_url=video_url.strip(),
        ))
    return result


def extract_list_page(url, name):
    """解析视频列表

    Args:
        url (string): 优酷页面地址
        name (string): 定时任务名称
    """
    html = http_get(url, timeout=10)
    if not html:
        return

    source, task_id = parse_task(name)
    try:
        videos = pars_list_page(html, source, task_id)
    except Exception as exc:
        statsd_client.incr('youku.extract.exc')
        logger.error('parse failure. url:{} name:{}'.format(url, name))
        logger.exception(exc)
    else:
        statsd_client.incr('youku.extract.suc')
        logger.info('parse success. url:{} name:{}'.format(url, name))
        new_videos = Videos.filter_exist(videos)
        return Videos.batch_add(new_videos)
