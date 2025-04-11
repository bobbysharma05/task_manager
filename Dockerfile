FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod -R 755 /app
RUN ls -la /app/manage.py
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]