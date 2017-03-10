# -*- coding=utf8 -*-
"""爬虫"""

from celery import Celery

app = Celery("spider")
app.config_from_object("spider.celeryconfig")
