# WARNING: This is experimental!
# Do not run in production yet
FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
# EXPOSE 80
# TODO: This will fail
RUN pip install --no-cache-dir -r requirements.txt
COPY manage.py manage.py
COPY ds ds
COPY dayliostats dayliostats

CMD [ "gunicorn", "dayliostats.wsgi" ]
