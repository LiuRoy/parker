# -*- coding: utf-8 -*-
"""视频存储"""
import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    SmallInteger,
    DateTime,
)
from spider.models import (
    DBSession,
    BaseModel,
)


class Videos(BaseModel):

    __tablename__ = 'web_video'

    id = Column(Integer, primary_key=True)
    source = Column(String(10), nullable=False)
    task_id = Column(Integer, nullable=False)
    img_url = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    video_url = Column(String(200), nullable=False)
    video_url_md5 = Column(String(32), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)

    @classmethod
    def filter_exist(cls, videos):
        """将已经存在表中的数据滤除

        Args:
            videos (list<WebVideo>): video 下载链接
        Returns:
            list<WebVideo> 返回不存在的视频链接
        """
        if not videos:
            return []

        video_url_md5s = [x.video_url_md5 for x in videos]
        session = DBSession()
        query_result = session.query(cls.video_url_md5).\
            filter(cls.video_url_md5.in_(video_url_md5s)).all()
        session.commit()
        exist_urls = {x[0] for x in query_result}
        return [x for x in videos if x.video_url_md5 not in exist_urls]

    @classmethod
    def batch_add(cls, videos):
        """批量添加记录

        Args:
            videos (list<WebVideo>): video 下载链接
        """
        if not videos:
            return

        records = [cls(
            source=x.source,
            task_id=x.task_id,
            img_url=x.img_url,
            duration=x.duration,
            title=x.title,
            video_url=x.video_url,
            video_url_md5=x.video_url_md5,
        ) for x in videos]
        session = DBSession()
        session.add_all(records)
        session.flush()
        session.commit()
        return records


class Information(BaseModel):

    __tablename__ = 'video_info'

    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, nullable=False)
    video_url = Column(String(200), nullable=False)
    format_ = Column(String(10), nullable=False)
    container = Column(String(10), nullable=False)
    profile = Column(String(10), nullable=False)
    size = Column(Integer, nullable=False, default=0)
    status = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    @classmethod
    def add(cls, video_format):
        """添加记录

        Args:
            video_format (VideoFormat): 格式信息
        """
        record = cls(
            video_id=video_format.video_id,
            video_url=video_format.video_url,
            format_=video_format.format,
            container=video_format.container,
            profile=video_format.profile,
            size=video_format.size
        )
        session = DBSession()
        session.add(record)
        session.flush()
        session.commit()
        return record

    @classmethod
    def update_status(cls, video_id, status=1):
        """添加记录

        Args:
            video_id (int): 视频id
            status (int): 1下载完成 0未下载
        """
        session = DBSession()
        target = session.query(cls).filter(cls.video_id == video_id)
        target.update({'status': status})
        session.commit()
