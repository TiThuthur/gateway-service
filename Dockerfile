FROM ubuntu:latest
LABEL authors="arthu"

ENTRYPOINT ["top", "-b"]