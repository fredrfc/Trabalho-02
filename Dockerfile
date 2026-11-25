FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    DATA_FILE=/data/arquivo.json

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY dados_exemplo.json ./

RUN mkdir -p /data

RUN useradd --create-home aluno \
    && chown -R aluno:aluno /app /data
USER aluno

CMD ["sh", "-ec", "[ -f \"$DATA_FILE\" ] || cp dados_exemplo.json \"$DATA_FILE\"; exec python main.py"]
