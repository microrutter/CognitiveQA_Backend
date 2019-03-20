# Use an official Python runtime as a parent image
FROM python:3.7.1-slim
WORKDIR /app
VOLUME /tmp
ADD . /app

# Install any needed packages specified in Pipfile.lock
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
