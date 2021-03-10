from sqlalchemy import Column, Integer, String
from config.db import Base, engine


class VoiceChannel(Base):
    __tablename__ = 'voice_channels'

    id = Column(Integer, primary_key=True)
    discord_id = Column(String(255))
    text_id = Column(String(255))
    guild_id = Column(String(255))
