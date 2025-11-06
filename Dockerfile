#Base Image 
FROM python:3.9

WORKDIR /usr/src/backend

COPY requirements.txt .
RUN pip install -r requirements.txt

# Download wait-for-it.sh for database waiting
RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && chmod +x wait-for-it.sh


COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]