FROM python:3.8

WORKDIR /usr/scr/sea_battle

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt .

RUN python -m venv . && \
    ls && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .


ENTRYPOINT ["./entrypoint.sh"]