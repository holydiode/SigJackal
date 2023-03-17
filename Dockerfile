FROM ubuntu:18.04
COPY ./ /app
RUN apt update
RUN apt -y upgrade
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.10
RUN apt install -y python3-pip
RUN pip install -y --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir -y
EXPOSE 8080
CMD python /app/web_gui.py