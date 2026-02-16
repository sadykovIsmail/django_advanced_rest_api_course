FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Create django-user
RUN adduser --disabled-password --gecos "" django-user

# Create static and media folders and give ownership to django-user
RUN mkdir -p /app/static /app/media && chown -R django-user:django-user /app/static /app/media

# Copy requirements separately for caching
COPY /app/requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ .

# Switch to django-user
USER django-user

# Expose port
EXPOSE 8000

# Default command
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
