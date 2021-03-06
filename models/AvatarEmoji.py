from sqlalchemy import Column, Integer, String
from config.db import Base, engine


class AvatarEmoji(Base):
    __tablename__ = 'profile_emoji'

    id = Column(Integer, primary_key=True)
    discord_id = Column(String)
    name = Column(String)
    user_id = Column(String)