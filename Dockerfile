FROM python:3.7.7-slim

RUN apt-get update && apt-get install -my wget gnupg curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Needed for libss1.0.0 and in turn MS SQL
RUN echo 'deb http://security.debian.org/debian-security jessie/updates main' >> /etc/apt/sources.list

# install necessary locales for MS SQL
RUN apt-get update && apt-get install -y locales \
    && echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen \
    && locale-gen

# install MS SQL related packages
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y gcc g++ debconf libcurl3 libc6 openssl libstdc++6 libkrb5-3 unixodbc unixodbc-dev msodbcsql17 mssql-tools libssl1.0.0

COPY requirements.txt /
COPY bin /bin

RUN pip3 install -r /requirements.txt

COPY covidmi /covidmi
WORKDIR /

ENTRYPOINT ["./bin/start.sh"]