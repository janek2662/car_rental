FROM --platform=linux/amd64 python:3.7-alpine

WORKDIR /car_rental

ADD . /car_rental

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

CMD ["python", "main.py"]