# Stage 1
FROM python:3.10-slim-buster AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
  && apt install --no-install-recommends gcc libpq-dev -y \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2
FROM python:3.10-slim-buster AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
  && apt install --no-install-recommends libpq5 -y \
  && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
RUN pip install psycopg2

COPY . /app/

# project's command
COPY /seed_data.py /app/
RUN python manage.py createsuperuser
RUN python manage.py shell < /app/seed_data.py

RUN python manage.py makemigrations
RUN python manage.py migrate


EXPOSE 8000

CMD ['gunicorn','test_api.wsgi:application','--bind','0.0.0.0:8000']
