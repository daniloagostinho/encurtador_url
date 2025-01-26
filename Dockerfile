# Usar uma imagem base leve do Python
FROM python:3.12-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos necessários
COPY requirements.txt ./

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte para dentro do container
COPY . .

# Expor a porta que o Uvicorn usará
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
