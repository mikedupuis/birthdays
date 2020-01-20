FROM python:alpine

RUN mkdir -p -m 0755 /apps/birthdays

ADD ./birthdays.py /apps/birthdays

VOLUME /apps/birthdays/data

CMD python3 /apps/birthdays/birthdays.py /apps/birthdays/data/birthdays.json
