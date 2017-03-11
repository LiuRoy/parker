# -*- coding: utf-8 -*-
"""用you-get库下载视频"""
import os
import re
import yaml
import subprocess

from spider.config.conf import params
from spider.tools.common import VideoInfo
from spider.models.videos import Information
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
        info_cmd = "you-get -i '{}'".format(play_url)
        output_info = os.path.join(params['download_path'],
                                   '{}.yaml'.format(video_id))
        p = subprocess.Popen(info_cmd, shell=True, stdout=subprocess.PIPE)
        content = p.stdout.read()
        content = content.replace(
            b'    [ DEFAULT ] _________________________________\n', b'')
        content = content.replace(b'\x1b[7m', b'')
        content = content.replace(b'\x1b[0m', b'')
        content = content.replace(b'\x1b[4m', b'')

        with open(output_info, 'w') as f:
            f.write(content.decode('utf-8'))

        with open(output_info, 'r') as f:
            video_info = yaml.load(f)
            default_format = video_info['streams'][0]

            video_format = VideoInfo(
                video_id=video_id,
                video_url=play_url,
                format=default_format['format'],
                container=default_format['container'],
                profile=default_format['video-profile'],
                size=parse_size(default_format['size'])
            )
    except Exception as exc:
        statsd_client.incr('youku.youget.info.exc')
        logger.error('you-get info failure: url:{} video:{}'.format(
            play_url, video_id))
        logger.error(exc)
    else:
        statsd_client.incr('youku.youget.info.suc')
        logger.info('you-get info success: url:{} video:{}'.format(
            play_url, video_id))
        #Format.add(video_format)
        return video_format


def download_video(video_format):
    """下载视频

    Args:
        video_format (VideoFormat): 视频下载信息
    """
    try:
        output_file = os.path.join(params['download_path'],
                                   '{}.{}'.format(video_format.video_id,
                                                  video_format.container))
        cmd = "you-get -O {} '{}'".format(output_file, video_format.video_url)
        subprocess.call(cmd, shell=True)
    except Exception as exc:
        statsd_client.incr('youku.youget.download.exc')
        logger.error('you-get download failure: url:{} video:{}'.format(
            video_format.video_url, video_format.video_id))
        logger.exception(exc)
    else:
        statsd_client.incr('youku.youget.download.suc')
        logger.info('you-get download success: url:{} video:{}'.format(
            video_format.video_url, video_format.video_id))
        #Format.update_status(video_format.video_id)
