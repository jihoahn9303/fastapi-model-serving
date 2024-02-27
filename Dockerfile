FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && mkdir -p /code/database \
    && mkdir -p /code/src

COPY ./main.py ./.env /code/
COPY database/ /code/database/
COPY src/ /code/src/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
