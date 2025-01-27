# 🚀 **System Design - Projeto Encurtador de URLs**

## 📌 Sobre o Projeto
Este projeto é um **Encurtador de URLs** desenvolvido com **FastAPI** no backend e utilizando **PostgreSQL** e **Redis** para armazenamento e cache. O objetivo é fornecer um sistema eficiente e escalável para encurtamento de links, permitindo redirecionamento rápido e armazenamento otimizado.

## 🛠️ Tecnologias Utilizadas
- **🐍 FastAPI** - Framework web assíncrono para Python.
- **🐘 PostgreSQL** - Banco de dados relacional para armazenamento persistente das URLs.
- **🛑 Redis** - Cache para otimizar acessos e reduzir carga no banco de dados.
- **🐳 Docker & Docker Compose** - Containerização e orquestração do ambiente.
- **🔗 SQLAlchemy** - ORM para interação com o banco de dados.
- **⚡ Uvicorn** - Servidor ASGI para rodar a API.

## 📂 Estrutura do Projeto
```
encurtador_url/
│-- app/
│   ├── main.py            # Arquivo principal da API
│   ├── database.py        # Configuração do PostgreSQL
│   ├── cache.py           # Configuração do Redis
│   ├── models.py          # Definição das tabelas do banco de dados
│   ├── routes.py          # Definição das rotas da API
│-- docker-compose.yml     # Configuração para rodar o ambiente Docker
│-- Dockerfile             # Configuração para criar imagem da API
│-- requirements.txt       # Lista de dependências do projeto
│-- README.md              # Documentação do projeto
```

## ⚙️ Como Rodar o Projeto
### 🔥 **Pré-requisitos**
Antes de iniciar, certifique-se de ter instalado:
- **Docker** e **Docker Compose**
- **Python 3.12** (caso queira rodar sem Docker)

### 🐳 **Rodando com Docker**
1️⃣ Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd encurtador_url
```
2️⃣ Suba os containers:
```bash
docker compose up -d
```
3️⃣ Teste a API:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8001/encurtar' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://www.exemplo.com"}'
```

### 🖥 **Rodando Localmente (Sem Docker)**
1️⃣ Instale as dependências:
```bash
pip install -r requirements.txt
```
2️⃣ Inicie o Redis e o PostgreSQL manualmente.
3️⃣ Configure as variáveis de ambiente no `.env` (ou modifique `database.py` e `cache.py`).
4️⃣ Execute a API:
```bash
uvicorn main:app --reload
```

## 📡 **Endpoints da API**
### 🔹 Criar uma URL encurtada
**POST** `/encurtar`
```json
{
  "url": "https://www.exemplo.com"
}
```
🔹 **Resposta:**
```json
{
  "short_url": "http://127.0.0.1:8001/XyZ123"
}
```

### 🔹 Acessar uma URL encurtada
**GET** `/{short_code}`
🔹 **Exemplo:**
```bash
curl -v http://127.0.0.1:8001/XyZ123
```

## 📌 Melhorias Futuras
✅ Implementação do frontend com Vue.js.  
✅ Adicionar métricas e monitoramento com Prometheus + Grafana.  
✅ Expiração de URLs encurtadas.  
✅ Relatórios de estatísticas de acesso.  
✅ Usar **NGINX ou Traefik** para distribuir requisições entre múltiplos containers.
✅ RabbitMQ ou Kafka para processar logs de acesso sem sobrecarregar a API
✅ Monitoramento e logs
---

### 💡 **Contribuição**
Sinta-se à vontade para contribuir! Faça um fork do repositório, crie uma branch e abra um pull request. Qualquer sugestão é bem-vinda. 😊

### 📜 **Licença**
Este projeto está sob a licença **MIT**.

💻 **Desenvolvido por [Seu Nome](https://github.com/seu-usuario)**

