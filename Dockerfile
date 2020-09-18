FROM python:3-slim

ADD *.px /

VOLUME [ "/config", "/data", "/log" ]

# dummy cmd to instantly terminate
# this is a tool image, containers should be run by triggering program invocation externally
# e.g. docker exec adamah python3 check_deliveries.py
CMD /bin/true