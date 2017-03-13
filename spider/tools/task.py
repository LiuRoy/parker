# -*- coding: utf-8 -*-
"""celery base task"""
import celery
from spider.config.conf import logger


class ParkerTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error("task {} error".format(task_id))
        logger.exception(exc)
        return super(ParkerTask, self).on_failure(
            exc, task_id, args, kwargs, einfo)

    def on_success(self, retval, task_id, args, kwargs):
        logger.info("task {} done".format(task_id))
        return super(ParkerTask, self).on_success(
            retval, task_id, args, kwargs)
