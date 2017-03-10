# -*- coding: utf-8 -*-
"""存储数据库"""
from spider.tools.db import make_session
from spider.config.conf import params
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()
DBSession = make_session(params['mysql_url'])
