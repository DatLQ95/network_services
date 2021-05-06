FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY NetData.py NetData.py
CMD [ "python3", "NetData.py", "--host=0.0.0.0"]