# Use uma imagem Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de dependências e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para o container
COPY . .

# Exponha a porta que o Flask vai rodar
EXPOSE 5000

# Comando para rodar a aplicação
# Comando para iniciar a aplicação Flask
CMD ["flask", "run", "--host=0.0.0.0"]
