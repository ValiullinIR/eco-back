FROM python:3.7-alpine


RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev musl-dev
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps
RUN apk update

RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 -m pip install --upgrade Pillow

EXPOSE 5000

ENTRYPOINT ["gunicorn","-b 0.0.0.0:5000","run:app"]
