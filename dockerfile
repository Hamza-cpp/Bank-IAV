FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN flask db upgrade head

EXPOSE  5000

CMD [ "python", "run.py" ]

# how can I run this dockerfile?
# docker build -t myapp .
# docker run -p 5000:5000 myapp