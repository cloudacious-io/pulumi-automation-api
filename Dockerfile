FROM python:latest as pulumi

RUN python --version

WORKDIR /code
RUN apt update

RUN python -m pip install --upgrade pip

RUN python -m pip install \
  boto3 \
  cloudaciousIAC \
  python-dotenv \
  pulumi-aws \
  pulumi-aws-native \
  pulumi-std \
  pulumi-docker 

RUN curl -fsSL https://get.pulumi.com | sh
ENV PULUMI_CONFIG_PASSPHRASE=""

COPY scripts/.bashrc .
RUN cat .bashrc >> /root/.bashrc
