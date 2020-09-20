FROM python:3-slim

ADD *.py /

VOLUME [ "/config", "/data", "/log" ]

CMD python3 check_deliveries.py