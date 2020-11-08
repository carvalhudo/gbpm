FROM python:3.6

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /etc/gur && touch /etc/gur/mirrors.csv
RUN echo "master,https://github.com/carvalhudo/gur-recipes.git" > /etc/gur/mirrors.csv
RUN mkdir -p /var/db/gur

WORKDIR /gur/gur
ENTRYPOINT ["/bin/bash"]
