# -*- coding: utf-8 -*-
"""用you-get库下载视频"""
import re
import subprocess

from spider.config.conf import params
from spider.tools.common import VideoInfo
from spider.models.videos import DownloadInfo
from spider.config.conf import (
    logger,
    statsd_client,
)


def parse_size(size_info):
    """解析视频大小信息

    Args:
        size_info (string): eg: 62.9 MiB (65951953 bytes)
    Returns:
        int
    """
    result = re.search(r'(\d+) bytes', size_info)
    if result:
        return int(result.group(1))
    return 0


def get_video_info(play_url, video_id):
    """获取视频信息

    Args:
        play_url (string): 播放地址
        video_id (int): 视频id
    """
    try:
        info_comd = "you-get -i {}".format(play_url)
        p = subprocess.Popen(info_comd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        content = p.stdout.read()
        content = content.decode('utf-8')

        video_title = re.search(r'Title:\s+(.*?)\s+Type:', content).group(1)
        video_size = int(re.search(r'\((\d+) Bytes\)', content).group(1))

        video_info = VideoInfo(
            video_id=video_id,
            video_url=play_url,
            title=video_title,
            size=video_size,
        )
        logger.info(video_info)
    except Exception as exc:
        statsd_client.incr('youget.info.exc')
        logger.error('you-get info failure: url:{} video:{}'.format(
            play_url, video_id))
        logger.error(exc)
    else:
        statsd_client.incr('youget.info.suc')
        logger.info('you-get info success: url:{} video:{}'.format(
            play_url, video_id))
        DownloadInfo.add(video_info)
        return video_info


def download_video(video_info):
    """下载视频

    Args:
        video_info (VideoInfo): 视频下载信息
    """
    try:
        download_comd = "you-get {}".format(video_info.video_url)
        p = subprocess.Popen(download_comd,
                             shell=True, cwd=params['download_path'])
        p.wait(int(params['download_timeout']))
    except Exception as exc:
        statsd_client.incr('youget.download.exc')
        logger.error('you-get download failure: url:{} video:{}'.format(
            video_info.video_url, video_info.video_id))
        logger.exception(exc)
    else:
        statsd_client.incr('youget.download.suc')
        logger.info('you-get download success: url:{} video:{}'.format(
            video_info.video_url, video_info.video_id))
        DownloadInfo.update_status(video_info.video_id)
