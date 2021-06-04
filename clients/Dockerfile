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
ENV PORT_NUMBER 8984
ENV USER_NO 100
ENV MEDIA_SERVICE 0


CMD [ "python3", "client.py"]