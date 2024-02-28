FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && mkdir -p /code/database \
    && mkdir -p /code/src \
    && mkdir -p /code/scripts

COPY database/ /code/database/
COPY src/ /code/src/
COPY .env ./main.py /code/
COPY ./scripts/*.sh /code/scripts/

RUN chmod +x /code/scripts/create_env.sh \
    && /code/scripts/create_env.sh \
    && --mount=type=secret,id=mysql_user \
        sed -i "s/MYSQL_USER=/MYSQL_USER=$(cat /run/secrets/mysql_user)" /code/.env \
    && --mount=type=secret,id=mysql_password \
        sed -i "s/MYSQL_PASSWORD=/MYSQL_PASSWORD=$(cat /run/secrets/mysql_password)" /code/.env \
    && --mount=type=secret,id=mysql_host \
        sed -i "s/MYSQL_HOST=/MYSQL_HOST=$(cat /run/secrets/mysql_host)" /code/.env \
    && --mount=type=secret,id=mysql_port \
        sed -i "s/MYSQL_PORT=/MYSQL_PORT=$(cat /run/secrets/mysql_port)" /code/.env \
    && --mount=type=secret,id=mysql_database_name \
        sed -i "s/MYSQL_DATABASE_NAME=/MYSQL_DATABASE_NAME=$(cat /run/secrets/mysql_database_name)" /code/.env

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
