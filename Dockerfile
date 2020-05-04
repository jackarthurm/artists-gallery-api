FROM python:3.7.2-alpine3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev
RUN apk add --no-cache \
    zlib \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev
RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN apk --purge del .build-deps

COPY . .

RUN adduser -D myuser
USER myuser

CMD gunicorn gallery_api.wsgi:application --bind 0.0.0.0:8000 --config gunicorn.conf.py
