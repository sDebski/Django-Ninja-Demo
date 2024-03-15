FROM python:3.10.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /app

RUN pip3 install poetry==1.6.1

COPY poetry.lock pyproject.toml /app/

RUN poetry export -f requirements.txt --output requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh"]