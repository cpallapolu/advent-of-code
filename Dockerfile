# if you're doing anything beyond your local machine,
# please pin this to a specific version at https://hub.docker.com/_/python/
FROM python:3.8-slim

ENV PATH /usr/local/bin:$PATH

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y make

RUN pip install --upgrade pip

# copy in our source code last, as it changes the most
WORKDIR /tmp/aoc
COPY . /tmp/aoc

RUN make pip-install

RUN make run-all-puzzles
