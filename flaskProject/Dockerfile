FROM python:3.10-slim

WORKDIR /flaskProject

COPY / /flaskProject

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from models import init_db; init_db()"

EXPOSE 8000

CMD ["python", "app.py"]


