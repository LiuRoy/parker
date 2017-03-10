# -*- coding: utf-8 -*-
"""celery配置"""

from spider.config.conf import (
    load_sites,
    params
)

# todo 解析配置文件生成
BROKER_URL = params['broker_url']

# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'

CELERY_IMPORTS = (
    'spider.parse',
    'spider.download',
    'spider.upload',
)

# todo 解析配置文件生成
CELERYBEAT_SCHEDULE = load_sites()
