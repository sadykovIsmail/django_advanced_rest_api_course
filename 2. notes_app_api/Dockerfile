#install python
FROM python:3.12

# run all commands in the app folder
WORKDIR /app

# copy everything from app folder
COPY ./app /app

# copy and run final steps
COPY  requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
