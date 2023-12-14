FROM python:3.10.4-slim-bullseye

# Set work directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . /app
CMD ["python", "main.py"]