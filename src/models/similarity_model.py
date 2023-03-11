from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Similarity(Base):
    __tablename__ = "similarity"

    id = Column(Integer, primary_key=True)
    similarity = Column(Float, nullable=False, default=0.9)
