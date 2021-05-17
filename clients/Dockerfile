FROM python:3.8-slim-buster

RUN apt-get update -y && apt-get install -y --no-install-recommends \
      bc \
      build-essential \
      ffmpeg \
      libssl-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY client.py client.py

ENV IP_ADDRESS 192.168.3.72
ENV PORT_NUMBER 8001
ENV USER_NO 100
ENV MEDIA_SERVICE 0


CMD [ "python3", "client.py", "--host=0.0.0.0"]