FROM python:3.6

COPY tests/requirements.txt /tmp/requirements_tests.txt
COPY requirements.txt /tmp/requirements.txt
RUN mkdir /etc/gbpm && touch /etc/gbpm/mirrors.csv
RUN mkdir -p /var/db/gbpm

WORKDIR /gbpm
RUN pip3 install -r /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements_tests.txt
ENTRYPOINT ["nose2", "-c", "/gbpm/tests/unit/nose.cfg"]
