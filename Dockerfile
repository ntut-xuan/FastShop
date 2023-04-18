FROM ubuntu:22.10
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# setup mirror
RUN sed 's@archive.ubuntu.com@free.nchc.org.tw@' -i /etc/apt/sources.list
# apt update
RUN apt-get update
RUN apt-get install -y ssh make build-essential net-tools curl git python3-pip
# install nodejs and npm
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash
RUN apt-get install nodejs
RUN node -v
RUN npm -v
# setup repository file to /etc/fastshop
RUN mkdir /etc/fastshop
COPY . /etc/fastshop
# make var-path directory to store static file.
RUN mkdir /var/fastshop
RUN mkdir /var/fastshop/image
# install tailwindcss and react.js from npm
WORKDIR /etc/fastshop
RUN npm install -D tailwindcss
RUN npm install babel-cli@6 babel-preset-react-app@3
# install pyhton package from pip
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD flask --debug --app backend/app:create_app run --host 0.0.0.0 --port 8080
