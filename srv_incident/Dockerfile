FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask requests flasgger

EXPOSE 5000

CMD ["python", "mod_srv_incident.py"]