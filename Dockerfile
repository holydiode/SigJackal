FROM python:3.10-alpine
COPY ./ /app
RUN apk update
RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev \
    libffi-dev openssl-dev
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir
EXPOSE 8080
CMD python /app/web_gui.py