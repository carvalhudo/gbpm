FROM python:3.8

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /etc/gur
RUN echo "master,https://github.com/carvalhudo/gur-recipes.git" > /etc/gur/mirrors
RUN mkdir -p /var/db/gur

WORKDIR /gur/gur
ENTRYPOINT ["/bin/bash"]
