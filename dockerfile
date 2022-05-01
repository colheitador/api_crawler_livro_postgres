FROM python:3.8.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
#requiremenets.txt == pip install fastapi & pip install uvicorn & pip install sqlite3 & pip install requests & pip install bs4 & pip install datetime

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
