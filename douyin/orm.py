# 程序创建@李宏宇
# 创建时间 ：2023/5/24
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建映射基类
Base = declarative_base()


# 定义模型类
class DouyinHot(Base):
    __tablename__ = 'tb_douyin_hot'

    名次 = Column(Integer, primary_key=True)
    热搜文本 = Column(String(255))
    标识 = Column(String(255))
    热度 = Column(String(255))
    采集时间 = Column(Date)
    抖音视频编号 = Column(String(255))
    点赞 = Column(Integer)
    评论 = Column(Integer)
    收藏 = Column(Integer)
    转发 = Column(Integer)
    作者账号昵称 = Column(String(255))
    作者账号id = Column(String(255))
    粉丝数 = Column(Integer)
    账号获赞 = Column(Integer)
