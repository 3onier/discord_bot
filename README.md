# Discord bot

this is my discord bot. It hasn't got any name yet.

## Development

### Prerequisites

- [Python](https://www.python.org/) >= 3.9
- [pipenv](https://pypi.org/project/pipenv/) >=  2020.11.15
- [Git](https://git-scm.com/)
- [Discordpy](https://discordpy.readthedocs.io) >= 1.6.0
- [SQLAlchemy](https://www.sqlalchemy.org/) >= 1.3.23

## Installation 

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