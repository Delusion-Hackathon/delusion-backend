FROM python:3.11-alpine as base
FROM base as builder
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM base

# RUN mkdir /app && \
#     addgroup --gid 1001 -S app && \
#     adduser -g "" -s /bin/false -D -u 1001 -S -G app app && \
#     chown -R app:app /app

# USER app
WORKDIR /app

RUN apk add libmagic
# COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
# RUN pip install --no-cache --no-cache-dir /wheels/*
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000


# Run the production server
CMD ["newrelic-admin", "run-program", "gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "delusion.wsgi:application"]
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1
