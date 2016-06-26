FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y vim make python3 python3-pip python3-venv
