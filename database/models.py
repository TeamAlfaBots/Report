from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True)
    api_id = Column(Integer)
    api_hash = Column(String)
    session_string = Column(Text)
    proxy_ip = Column(String, default="0.0.0.0")
    proxy_port = Column(Integer, default=0)
    is_active = Column(Integer, default=1)

class Target(Base):
    __tablename__ = 'targets'
    id = Column(Integer, primary_key=True)
    target_type = Column(String) # user, channel, group
    target_id = Column(String)
    reason = Column(String)
    status = Column(String, default="pending")

engine = create_engine('sqlite:///deephat_bot.db')
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
