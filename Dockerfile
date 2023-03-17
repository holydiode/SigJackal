FROM python:3.9-slim
COPY ./ /app
RUN apt update
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir
EXPOSE 8080
CMD python /app/web_gui.py