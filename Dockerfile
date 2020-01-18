FROM python:alpine

RUN mkdir -p -m 0755 /apps/birthdays

ADD ./birthdays.py /apps/birthdays

VOLUME /apps/birthdays/data

RUN pip3 install python-dateutil

CMD python3 /apps/birthdays/birthdays.py /apps/birthdays/data/birthdays.json
