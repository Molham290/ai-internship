
FROM python:3.11-slim



RUN apt-get update && apt-get install -y curl zstd
RUN curl -fsSL https://ollama.com/install.sh | sh


RUN ollama serve & sleep 5 && ollama pull llama3


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir ollama


RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install fpdf2 ollama --break-system-packages


ENV OLLAMA_HOST=0.0.0.0

CMD ["bash", "-c", "ollama serve"]