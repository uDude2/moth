FROM python:3

WORKDIR /usr/local/src
RUN git clone https://github.com/dirtbags/moth/

WORKDIR /moth
ENTRYPOINT ["python3", "/usr/local/src/moth/tools/devel-server.py"]
