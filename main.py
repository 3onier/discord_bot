import os
import bot

import migrate

if __name__ == '__main__':
    migrate.migrate()
    bot.bot.run(os.getenv("TOKEN"))
