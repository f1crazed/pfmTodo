FROM debian:latest


RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install libexpat1  -y
RUN apt-get install build-essential -y
RUN apt-get install apache2 -y
RUN apt-get install apache2-utils -y
RUN apt-get install libapache2-mod-wsgi-py3 -y
RUN apt-get install vim -y
RUN apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip


COPY pfmtodo.conf /etc/apache2/sites-available/apache-flask.conf

RUN a2enmod headers

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt


RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf
RUN service apache2 restart

EXPOSE 80

CMD  /usr/sbin/apache2ctl -D FOREGROUND


#CMD ./startapp.sh

# docker build -t pfmtodo-app .
# docker run -d -p 5000:5000 -v C:/Users/Jeremy/Dev/pfmTodo:/app --name pfmtodo-server pfmtodo-app
# docker run -d -p 5000:5000 -v /Users/jeremy/Development/pfmTodo/pfmTodo:/app --name pfmtodo-server pfmtodo-app

