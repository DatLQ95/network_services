FROM python:3

WORKDIR /usr/src/app

RUN apt-get update -y && apt-get install -y --no-install-recommends \
      bc \
      build-essential \
      ffmpeg \
      libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY client.py client.py

ENV IP_ADDRESS 131.155.35.54

ENV SEARCH_PORT 8001
ENV SHOP_PORT 8002
ENV WEB_PORT 8003
ENV MEDIA_PORT 8004

ENV SEARCH_USER_NO 5
ENV SHOP_USER_NO 5
ENV WEB_USER_NO 5
ENV MEDIA_USER_NO 5

ENV MEDIA_SERVICE 0


CMD [ "python3", "client.py"]