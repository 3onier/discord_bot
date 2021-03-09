FROM python:3.9.2

# create env variables
ENV SQLITE_PATH="data/data.db"

WORKDIR /bot/
RUN mkdir /bot/data

RUN mkdir bin

# copy files to image
COPY cogs bin/cogs
COPY models bin/models
COPY config bin/config
COPY bot.py bin/
COPY main.py bin/
COPY migrate.py bin/
COPY requirements.txt .


# upgrade pip
RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

WORKDIR /bot/bin/

RUN python migrate.py

CMD python main.py