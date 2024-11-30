# ======================================================================
# Base
# ======================================================================
FROM public.ecr.aws/amazonlinux/amazonlinux:2023 as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TZ :/etc/localtime
ENV PATH /var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/opt/bin:/usr/sbin/
ENV LD_LIBRARY_PATH /var/lang/lib:/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONFAULTHANDLER 1

COPY requirements.yum .
RUN yum -y -q update && yum -y -q upgrade &&\
    yum -y -q install --nodocs passwd util-linux-user findutils &&\
    sed 's/#.*//' requirements.yum | xargs yum -y -q install --nodocs &&\
    passwd -d root && adduser python &&\
    yum -y -q clean all && rm -rf /var/lib/yum/* /tmp/* /var/tmp/*


# ======================================================================
# Builder
# ======================================================================
FROM base as builder

RUN yum -y -q install --nodocs pip make automake gcc gcc-c++ git which &&\
    yum -y -q clean all && rm -rf /var/lib/yum/* /tmp/* /var/tmp/*

RUN mkdir -p -m 0600 ~/.ssh &&\
    touch ~/.ssh/known_hosts &&\
    ssh-keygen -F bitbucket.org || ssh-keyscan -t rsa bitbucket.org >> ~/.ssh/known_hosts &&\
    ssh-keygen -F github.com || ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts &&\
    ssh-keygen -F gitlab.com || ssh-keyscan -t rsa gitlab.com >> ~/.ssh/known_hosts

# Project dependency
ENV PATH $PATH:/root/.local/bin
ENV PIP_ROOT_USER_ACTION ignore
RUN pip install -q --compile --user --upgrade pip pipenv

# WORKDIR /root/project
COPY Pipfile* .

ENV PATH $PATH:/.venv/bin
ENV PIPENV_VENV_IN_PROJECT 1
RUN pipenv install --python=/bin/python3.11 --dev


# ======================================================================
# Runtime
# ======================================================================
FROM base AS runtime

ENV DJANGO_COLORS dark

# Creating workspace
ENV HOME /home/python
ENV WORKSPACE $HOME/application
RUN mkdir -p $WORKSPACE && chown -R python:python $WORKSPACE
WORKDIR $WORKSPACE

# Project dependency
COPY --chown=python:python --from=builder /.venv /.venv
ENV PATH /.venv/bin:$PATH

# Copy project
COPY --chown=python:python ./application $WORKSPACE

USER python

RUN mkdir -p media && chown -R python:python media &&\
    mkdir -p static && chown -R python:python static

# Creating environment variable: RELEASE
ARG release=undefined
ENV RELEASE=$release
