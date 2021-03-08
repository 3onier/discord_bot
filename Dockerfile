FROM python:3.9.2

# create env variables
ENV SQLITE_PATH="data/data.db"

WORKDIR bot/
RUN mkdir data

RUN mkdir bin

# copy files to image
COPY cogs bin/
COPY models bin/
COPY config bin/
COPY bot.py bin/
COPY main.py bin/
COPY migrate.py bin/
COPY requirements.txt .


# upgrade pip
RUN python -m pip --upgrade pip

RUN python -m pip install -r requirements.txt

RUN python bin/migrate.py

CMD python bin/main.py