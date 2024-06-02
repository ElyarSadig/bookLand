FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port on which Gunicorn will run
EXPOSE 8000

# Start Gunicorn with your Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bookLand_microservice.wsgi:application"]
