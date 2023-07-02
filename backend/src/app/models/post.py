from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime

from app.db.base_class import Base


class Post(Base):
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime, nullable=False, default=datetime.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='items', lazy='selectin')
    comments = relationship('Comment', back_populates='post', lazy="selectin")
