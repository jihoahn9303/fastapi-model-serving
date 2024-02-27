FROM python:3.9

RUN mkdir -p /code/app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 

COPY ./database/ ./main.py /code/app
COPY .env /code

WORKDIR /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
