# -*- coding: utf-8 -*-
"""解析sites.yaml"""
import os
import yaml
import logging
import logging.config
from datetime import timedelta

import statsd
from spider.tools.statsd import FakeStatsdClient

current_dir = os.path.dirname(__file__)
sites_path = os.path.join(current_dir, 'sites.yaml')
params_path = os.path.join(current_dir, 'params.yaml')
logging_path = os.path.join(current_dir, 'logging.yaml')

with open(logging_path, 'r') as f:
    logging.config.dictConfig(yaml.load(f))


def load_sites():
    """解析sites.yaml 生成CELERYBEAT_SCHEDULE"""
    with open(sites_path, 'r') as f:
        sites = yaml.load(f)
        return {x['name']: {
            'task': x['task'],
            'schedule': timedelta(minutes=int(x['minute'])),
            'args': (x['url'], )
        } for x in sites['sites']}


def load_params():
    """解析params.yaml"""
    with open(params_path, 'r') as f:
        p = yaml.load(f)
        return p['params'][0]


params = load_params()
if params['mode'] == 'debug':
    logger = logging.getLogger('parker.debug')
    statsd_client = FakeStatsdClient()
else:
    logger = logging.getLogger('parker.release')
    statsd_host, statsd_port = params['statsd_address'].split(':')
    statsd_client = statsd.StatsClient(
        host=statsd_host, port=int(statsd_port), prefix='parker')
