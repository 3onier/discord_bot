# Discord bot

this is my discord bot. It hasn't got any name yet.

## Development

### Prerequisites

- [Python](https://www.python.org/) >= 3.9
- [pipenv](https://pypi.org/project/pipenv/) >=  2020.11.15
- [Git](https://git-scm.com/)
- [Discordpy](https://discordpy.readthedocs.io) >= 1.6.0
- [SQLAlchemy](https://www.sqlalchemy.org/) >= 1.3.23
- [Docker](https://www.docker.com/) (recommended)
- [docker-compose](https://docs.docker.com/compose/) (recommended)

## Installation 

### with docker

```
# clone git repository
git clone https://github.com/3onier/discord_bot

cd discord_bot

# adjust setting if needed
nano Dockerfile
nano docker-compose.yml

# build ducker image
sudo docker build . -t 3onier/discord_bot

# run cointainer
docker-compose up -d

```

### local

```
# clone git repository
git clone https://github.com/3onier/discord_bot

# create virtual enviroment
pipenv install

# migrate database
pipenv run migrate
```

## Environment variables

| Name      | Description | Default |
|:----------|:------------|:--------|
|TOKEN      |Token for the Discord bot API|     |
|SQLITE_PATH      |Path to sqlite file| "../data/data.db"     |