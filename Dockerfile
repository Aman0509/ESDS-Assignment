FROM python

RUN  pip3 install Django==3.1.5

RUN pip3 install psycopg2

RUN pip3 install djangorestframework

WORKDIR /djangoapp

COPY . .

WORKDIR /djangoapp/fake_bank

EXPOSE 8000

