FROM python:3.10-alpine
COPY ./ /app
RUN apk update
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir
EXPOSE 8080
CMD python /app/web_gui.py