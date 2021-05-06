FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY Prometheous.py Prometheous.py
CMD [ "python3", "Prometheous.py", "--host=0.0.0.0"]