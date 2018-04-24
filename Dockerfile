FROM python:3

WORKDIR /app

ADD . /app

RUN pip install bzt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "server.py"]
