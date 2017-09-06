FROM python:3-alpine

RUN apk --no-cache add git

WORKDIR /usr/local/src
RUN git clone https://github.com/dirtbags/moth/

RUN mkdir -p /moth/src
RUN cp -r moth/src/www /moth/src/www
RUN cp -r moth/example-puzzles /moth/puzzles
RUN cp -r moth/tools /moth/tools
RUN rm -rf moth

WORKDIR /moth
ENTRYPOINT ["python3", "/moth/tools/devel-server.py"]
