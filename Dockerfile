FROM python:3.12-slim

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY classes.py .

COPY equipamentos.py .

COPY excecoes.py .

COPY inventario.py .

COPY main.py .

COPY risco.py .

COPY vulnerabilidade.py .

EXPOSE 8000

CMD ["python", "main.py"]