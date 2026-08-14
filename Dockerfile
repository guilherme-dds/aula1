# Imagem base oficial do Python (versão slim para manter a imagem leve)
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Define variáveis de ambiente para desativar a gravação de arquivos .pyc e garantir logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copia e instala as dependências (aproveita o cache de camadas do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte para o container
COPY . .

# Expõe a porta em que a aplicação Flask executa
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
