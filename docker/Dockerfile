FROM python:3.9.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_DIR=/app 
ENV PYTHONPATH=$PYTHONPATH:$APP_DIR
COPY requirements-dev.txt requirements.txt ./
RUN pip install -U --user pip && pip install --user -r requirements-dev.txt 

WORKDIR ${APP_DIR}
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
EXPOSE 8000