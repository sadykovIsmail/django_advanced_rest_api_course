#install python
FROM --platform=linux/amd64 python:3.12

# tells to python don't write pyc codes like cache which we don't need
ENV PYTHONDONTWRITEBYTECODE=1

# to display error message for debugging
ENV PYTHONUNBUFFERED=1

# run all commands in the app folder
WORKDIR /app

# create user
RUN adduser --disabled-password --gecos "" django-user

# create media and static folders and give ownership to django user
RUN mkdir -p app/static app/media && chown -R django-user:django-user app/static app/media

# copy everything from requirements folder
COPY app/requirements.txt .

# upgrade pip and install from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
# make user django user
USER django-user

# expose port so it runs in 8000
EXPOSE 8000

# default command
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
