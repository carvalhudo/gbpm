FROM python:3.8

COPY tests/requirements.txt /tmp/requirements_tests.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements_tests.txt

RUN mkdir /etc/gur && touch /etc/gur/mirrors
RUN mkdir -p /var/db/gur

WORKDIR /gur/tests/unit
ENTRYPOINT ["nose2", "-c", "nose.cfg"]
