FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    DATA_FILE=/data/arquivo.json

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

RUN mkdir -p /data

RUN useradd --create-home aluno \
    && chown -R aluno:aluno /app /data
USER aluno

CMD ["python", "main.py"]
