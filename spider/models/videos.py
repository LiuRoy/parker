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

    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    publisher = Column(String(20), nullable=False, default='')
    source = Column(String(10), nullable=False)
    task_id = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False, default=0)
    star_count = Column(Integer, nullable=False, default=0)
    play_count = Column(Integer, nullable=False, default=0)
    img_url = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    publish_date = Column(DateTime, nullable=True)
    video_url = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)

    @classmethod
    def filter_exist(cls, videos):
        """将已经存在表中的数据滤除

        Args:
            videos (list<VideoInfo>): video 下载链接
        Returns:
            list<VideoInfo> 返回不存在的视频链接
        """
        if not videos:
            return []

        video_urls = [x.video_url for x in videos]
        session = DBSession()
        query_result = session.query(cls.video_url).\
            filter(cls.video_url.in_(video_urls)).all()
        session.commit()
        exist_urls = {x[0] for x in query_result}
        return [x for x in videos if x.video_url not in exist_urls]

    @classmethod
    def batch_add(cls, videos):
        """批量添加记录

        Args:
            videos (list<VideoInfo>): video 下载链接
        """
        if not videos:
            return

        records = [cls(
            publisher=x.publisher,
            source=x.source,
            task_id=x.task_id,
            comment_count=x.comment_count,
            star_count=x.star_count,
            play_count=x.play_count,
            img_url=x.img_url,
            duration=x.duration,
            title=x.title,
            publish_date=x.publish_date,
            video_url=x.video_url,
        ) for x in videos]
        session = DBSession()
        session.add_all(records)
        session.flush()
        session.commit()
        return records


class Format(BaseModel):

    __tablename__ = 'format'

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
