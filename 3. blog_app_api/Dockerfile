FROM python:3.12

# Set working directory
WORKDIR /app

# Copy everything from local 'app' folder
COPY ./app /app

# Copy requirements separately for caching
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
