FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set working directory
WORKDIR /app

# Copy everything from local 'app' folder
# Copy requirements separately for caching
COPY /app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN adduser --disabled-password --no-create-home django-user
USER django-user

EXPOSE 8000
# Default command
CMD ["gunicorn", "blog.wsgi:application", "--bind", "0.0.0.0:8000"]
