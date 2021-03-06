from config.db import engine, Base

# do not remove important for creation
from models import ProfileEmoji, VoiceChannel

Base.metadata.create_all(engine)
