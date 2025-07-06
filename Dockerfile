FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/home/app
RUN mkdir $APP_HOME

RUN apt update -y
RUN apt install build-essential libssl-dev libffi-dev libpq-dev libmagic1 libcairo2 -y

WORKDIR $APP_HOME

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry
RUN poetry install --no-root

RUN pip install uvicorn

COPY . $APP_HOME

RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh
ENTRYPOINT ["/home/app/entrypoint.sh"]
