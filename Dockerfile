FROM python:3.8-alpine

RUN apk add --no-cache gcc musl-dev python3-dev linux-headers


WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install Flask flask-prometheus-metrics
RUN pip install psutil

EXPOSE 5000

CMD ["python", "server.py"]
