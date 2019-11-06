FROM python


# RUN apt-get update
# RUN apt-get upgrade -y
RUN pip3 install --upgrade pip
RUN pip3 install setuptools

RUN mkdir /app


WORKDIR /app


COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=pfmtodo.py
ENV FLASK_DEBUG=1
ENV FLASK_RUN_PORT=5000

CMD flask run --host 0.0.0.0

#CMD ./startapp.sh

# docker build -t pfmtodo-app .
# docker run -d -p 5000:5000 -v C:/Users/Jeremy/Dev/pfmTodo:/app --name pfmtodo-server pfmtodo-app
# docker run -d -p 5000:5000 -v /Users/jeremy/Development/pfmTodo/pfmTodo:/app --name pfmtodo-server pfmtodo-app

