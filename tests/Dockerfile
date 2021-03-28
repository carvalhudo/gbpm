FROM python:3.6

COPY tests/requirements.txt /tmp/requirements.txt
RUN mkdir /etc/gbpm && touch /etc/gbpm/mirrors.conf

WORKDIR /gbpm
RUN pip3 install -r /tmp/requirements.txt
ENTRYPOINT ["nosetests", "-c", "/gbpm/tests/unit/nose.cfg"]
