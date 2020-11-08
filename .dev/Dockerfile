FROM python:3.6

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /etc/gbpm && touch /etc/gbpm/mirrors.csv
RUN echo "i3-gaps,https://github.com/carvalhudo/gbpm-packages.git" > /etc/gbpm/mirrors.csv
RUN mkdir -p /var/db/gbpm

WORKDIR /gbpm
ENTRYPOINT ["/bin/bash"]
