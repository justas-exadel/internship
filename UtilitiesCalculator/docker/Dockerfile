# specify the image you want to use build docker image

FROM python:3.8.1

# Maintainer name to let people know who made this image.

MAINTAINER Gertruda <viskoniekas@gmail.com>

#apt is the ubuntu command line tool for advanced packaging tool(APT) for sw upgrade '''

RUN apt update && \
    apt install -y netcat-openbsd

RUN apt-get install -y wget xz-utils libxrender1 libfontconfig1

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz

RUN tar -xf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz

RUN cp wkhtmltox/bin/wkhtmltopdf /usr/bin/wkhtmltopdf

RUN chmod a+x /usr/bin/wkhtmltopdf

RUN rm -rf wkhtmltox

# set the env variable to tell where the app will be installed inside the docker

ENV INSTALL_PATH /Photos-Docker-Flask
RUN mkdir -p $INSTALL_PATH

#this sets the context of where commands will be ran in and is documented

WORKDIR $INSTALL_PATH

# Copy in the application code from your work station at the current directory
# over to the working directory.

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p Photos-Docker-Flask/reports

RUN chmod +x /Photos-Docker-Flask/docker-entrypoint.sh

CMD ["/bin/bash", "/Photos-Docker-Flask/docker-entrypoint.sh"]
