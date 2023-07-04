FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update && apt install -y sqlite3

RUN pip install -r requirements.txt

COPY . .

RUN python3 -c "import secrets; print('SECRET_KEY = ', '\"', secrets.token_hex(), '\"', sep='')" > .env

RUN pip install waitress

EXPOSE 8080

CMD ["waitress-serve", "--url-scheme", "https", "--call", "flaskr:create_app"]
