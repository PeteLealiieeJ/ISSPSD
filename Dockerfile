FROM python:3.9

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]
