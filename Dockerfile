FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 

COPY ./src/ ./database/ ./main.py /code/app
COPY ./.env /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
