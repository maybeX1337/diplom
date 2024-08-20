FROM python:3.10-slim
ENV TZ="Europe/Moscow"
COPY requirements.txt /temp/reqs.txt
COPY . /main_dir

WORKDIR main_dir

RUN pip install -r /temp/reqs.txt


CMD ["fastapi", "run", "src/main.py"]