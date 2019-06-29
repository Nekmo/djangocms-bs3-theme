FROM python:3.5

ENV PYTHONUNBUFFERED 1

# RUN apt-get install debian-archive-keyring && apt-get update && apt-get dist-upgrade
RUN apt-get update
RUN apt-get install gettext -y
WORKDIR /tmp
COPY requirements.txt .
RUN echo "Installing requirements"
RUN pip install -r requirements.txt
RUN mkdir -p /var/log/gunicorn

ENV PYTHONPATH "/code:${PYTHONPATH}"
WORKDIR /code
ENTRYPOINT ["./entrypoint.py", "-w", "4", "-b", "0.0.0.0:8000", "demo_app.wsgi:application"]
