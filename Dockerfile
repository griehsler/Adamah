FROM python:3

ADD *.py requirements.txt /

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

VOLUME [ "/config", "/data", "/log" ]

CMD python3 check_deliveries.py