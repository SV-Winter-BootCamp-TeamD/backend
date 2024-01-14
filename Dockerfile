FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get update && \
    apt-get install -y libgl1-mesa-glx

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]