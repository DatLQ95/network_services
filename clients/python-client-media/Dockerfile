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
CMD [ "python3", "client.py", "--host=0.0.0.0"]