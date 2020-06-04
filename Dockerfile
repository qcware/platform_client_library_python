FROM python:3.7-slim-buster AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip

FROM base AS python-deps
RUN apt-get update && apt-get -y install git
COPY ./deploy_keys /root/.ssh
RUN chmod 600 /root/.ssh/quasar_deploy_rsa

RUN mkdir /setup && mkdir /setup/python_client
COPY ./python_client/requirements.txt /setup/python_client/requirements.txt
RUN pip install -r /setup/python_client/requirements.txt
RUN pip install pytest pytest-asyncio

COPY ./python_client /setup/python_client
RUN pip install -e /setup/python_client

#COPY ./deploy_keys /root/.ssh
#RUN chmod 600 /root/.ssh/quasar_deploy_rsa
#RUN pip install git+ssh://git@github.com:/qcware/quasar.git@platform

#CMD pytest /setup/python_client/tests
# the client doesn't do anything run by itself; otherwise
# if we run tests within the client by default, bringing
# the whole stack up fails (which happens because it can't
# communicate
CMD /bin/bash

