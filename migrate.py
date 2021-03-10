from config.db import engine, Base

# do not remove important for creation
from models import AvatarEmoji, VoiceChannel


def migrate():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    migrate()
