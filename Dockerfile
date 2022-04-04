FROM python:3.9

ENV PYTHONUNBUFFERED 1
#COPY ./requirements.txt /requirements.txt

RUN mkdir /project

COPY . /project

WORKDIR /project

RUN pip install --no-cache-dir -r requirements.txt

CMD python -m pytest -v /project