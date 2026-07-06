
FROM python:3.11-slim



RUN apt-get update && apt-get install -y curl zstd
RUN curl -fsSL https://ollama.com/install.sh | sh


RUN ollama serve & sleep 5 && ollama pull llama3


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir ollama


CMD bash -c "ollama serve & sleep 5 && python -u Task3_SelfContained.py"

CMD ["bash", "-c", "ollama serve & sleep infinity"]