FROM python:3.8-slim

WORKDIR /src

COPY requirements.txt .

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/* \
    && rm -rf requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]