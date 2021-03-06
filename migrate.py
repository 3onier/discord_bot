from config.db import engine, Base

# do not remove important for creation
from models import AvatarEmoji, VoiceChannel

Base.metadata.create_all(engine)
