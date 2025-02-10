FROM python:3.12-slim-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./source_model /code/source_model

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "8080"]