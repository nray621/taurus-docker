FROM python:3

WORKDIR /app

ADD . /app

RUN pip install bzt

RUN wget http://download.joedog.org/siege/siege-4.0.4.tar.gz && \
    tar zxvf siege-4.0.4.tar.gz

WORKDIR siege-4.0.4

RUN ./configure --with-ssl && make && make install

WORKDIR /app

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "server.py"]
