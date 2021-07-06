# Use an official Python runtime as a parent image
FROM python:3.8
WORKDIR /app
VOLUME /tmp
ADD . /app

# Install any needed packages specified in Pipfile.lock
RUN pip install pipenv
RUN pipenv install --system --deploy
CMD ["python", "app.py"]
