FROM python:3.10.14-slim-bullseye

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8800

CMD ["flet", "run", "--web", "--port", "8800", "todo.py"]