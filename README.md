# Challenge Geospatial

Uma API RESTful para gerenciar e consultar locais geográficos usando Flask, Nominatim (OpenStreetMap) e SQLite com suporte a SpatiaLite.

## Tecnologias

- **Flask** + **Flask-RESTX** – Framework web
- **SQLite** + **SpatiaLite** – Banco de dados espacial
- **Nominatim API** – Geocodificação via OpenStreetMap
- **Pydantic** – Validação de entrada e saída
- **Pytest** – Testes automatizados
- **Task** – Atalhos para execução de tarefas

---

## Funcionalidades

- Adicionar novos locais usando um nome (geocodificado automaticamente com Nominatim)
- Listar todos os locais armazenados
- Atualizar ou remover um local
- Buscar locais próximos dentro uma latitude e longitude com um raio definido
- Filtro espacial com bounding box e fórmula de Haversine
---

## Estrutura do Projeto

```
app/
├── controllers/        # Rotas
├── controllers/swagger/# Documentação Swagger
├── database/           # Conexão com o banco de dados e utils para SQLite
├── external/           # Integração com API Nominatim
├── repositories/       # Camada de acesso aos dados
├── services/           # Regras de negócio
├── schemas/            # Validação de dados com Pydantic
├── main.py             # Ponto de entrada da aplicação
├── config.py           # Configuração via dotenv
├── registry.py         # Injeção de dependências
├── logger.py           # Configuração do logger
scripts/
└── init_db_spatial.sh  # Script de criação do banco spatial
tests/
└── ...                 # Testes
```

---

## Setup

### 1. Clone o repositório

```bash
git clone https://github.com/matheuss0xf/challenge-geospatial.git
cd challenge-geospatial
```
### Pré-requisitos

- Docker
- Python 3.12+
- Poetry (para gerenciar dependências)

### Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
NOMINATIM_API=https://nominatim.openstreetmap.org/search
DATABASE=locations.db
HOST='0.0.0.0'
PORT='5000'
DEBUG='True/False'
```

### Subir o ambiente

```bash
docker-compose up --build
```

---

### Documentação Swagger disponível em:  
[http://localhost:5000/api/v1/docs](http://localhost:5000/api/v1/docs)

![image](https://github.com/user-attachments/assets/c45ab5fd-053f-455e-830b-f942919138d7)

---

## Executando os testes

```bash
poetry shell
task test
```

---
![challenge (0)](https://github.com/user-attachments/assets/537724a4-c907-48e3-a6d9-c9647b499876)
---

## Licença

Licença MIT.  
Dados geográficos fornecidos por OpenStreetMap & Nominatim — use com responsabilidade e credite adequadamente.
