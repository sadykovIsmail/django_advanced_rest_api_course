# light weight python image
FROM python:3.12-slim

# prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# everythin in app folder
WORKDIR /app

# install system dependincies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY ./app /app

# run the server
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
