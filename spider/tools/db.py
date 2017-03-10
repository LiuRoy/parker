from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine


def make_session(db_url):
    """根据数据库配置生成会话对象"""
    engine = create_engine(db_url)
    return sessionmaker(bind=engine)
