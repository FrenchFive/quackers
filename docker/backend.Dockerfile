FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./backend /app/

RUN mkdir "/db"

RUN pip install --no-cache-dir -r ./requirements.txt


CMD [ "python", "./src/main.py" ]