# -*- coding: utf-8 -*-
"""celery配置"""

from spider.config.conf import (
    load_sites,
    params
)

BROKER_URL = params['broker_url']

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_IMPORTS = (
    'spider.parse',
    'spider.download',
)

CELERYBEAT_SCHEDULE = load_sites()

CELERY_TASK_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
