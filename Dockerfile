FROM python:3.7.2-alpine3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        postgresql-dev \
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
        fribidi-dev \
    && python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

ADD . /app

EXPOSE 8000

ENTRYPOINT [ \
    "/usr/local/bin/gunicorn", \
        "--config", "/app/gunicorn.conf", \
        "-b", ":8000", \
    "gallery_api.wsgi:application" \
]
