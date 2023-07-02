from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime

from app.db.base_class import Base

class User(Base):
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('Post', back_populates='user', lazy='selectin')