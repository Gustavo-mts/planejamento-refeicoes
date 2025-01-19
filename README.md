# Gerenciador de Receitas - Documentação

## Configuração do Ambiente

### 1. Clone o Repositório

```bash
# Substitua pelo URL real do repositório
git clone https://github.com/Gustavo-mts/planejamento-refeicoes.git
cd planejamento-refeicoes
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv .venv
```

Ative o ambiente virtual:

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```
- **Linux/Mac**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

---

## Configuração do Banco de Dados

### 1. Configure o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```plaintext
DATABASE_URL=sqlite:///./data/sample_data.sqlite
```

Isso define o caminho para o banco de dados SQLite.

### 2. Crie o Diretório para o Banco

Se o diretório `data` não existir, crie-o:

```bash
mkdir data
```

### 3. Inicialize o Banco de Dados

Execute o comando abaixo para criar as tabelas no banco:

```bash
python -c "from app.database import init_db; init_db()"
```

Após esse comando, o arquivo do banco será criado em `data/sample_data.sqlite`.

---

## Inicialização do Servidor

Para iniciar o servidor FastAPI, execute:

```bash
uvicorn app.main:app --reload
```

O servidor ficará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000).

Você pode acessar a documentação interativa da API em:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Consultando o Banco de Dados

### 1. Usando o Terminal com `sqlite3`

Abra o banco de dados no terminal:

```bash
sqlite3 data/sample_data.sqlite
```

Liste as tabelas:

```sql
.tables
```

Exiba os dados de uma tabela (ex.: `receita`):

```sql
SELECT * FROM receita;
```

Saia do terminal SQLite:

```sql
.exit
```

### 2. Usando Ferramentas Gráficas

Use ferramentas como [DB Browser for SQLite](https://sqlitebrowser.org/) ou extensões do VS Code para explorar o banco de dados visualmente.

---

## Estrutura do Projeto

### Diretórios Principais

```plaintext
.
├── app/
│   ├── __init__.py
│   ├── main.py               # Inicialização da API
│   ├── config.py             # Configurações de ambiente
│   ├── database.py           # Conexão com o banco de dados
│   ├── models/               # Modelos SQLModel
│   │   ├── __init__.py
│   │   ├── ingrediente.py    # Modelo Ingrediente
│   │   ├── receita.py        # Modelo Receita
│   │   └── planejamento.py   # Modelo Planejamento
│   ├── routers/              # Rotas da API
│   │   ├── __init__.py
│   │   ├── ingrediente.py    # Rotas para Ingrediente
│   │   ├── receita.py        # Rotas para Receita
│   │   └── planejamento.py   # Rotas para Planejamento
│   └── utils.py              # Funções auxiliares
├── data/                     # Diretório para o banco SQLite
├── .env                      # Variáveis de ambiente
├── requirements.txt          # Dependências do projeto
└── README.md                 # Instruções do projeto
```

---

## Testando a API

### Testar com `curl`

- **Listar todas as receitas**:
  ```bash
  curl http://127.0.0.1:8000/receitas/
  ```

- **Criar uma nova receita**:
  ```bash
  curl -X POST http://127.0.0.1:8000/receitas/ \
  -H "Content-Type: application/json" \
  -d '{
      "nome": "Bolo de Chocolate",
      "tempo_preparo": 60,
      "descricao": "Um bolo delicioso.",
      "porcoes": 8,
      "nivel_dificuldade": "Médio",
      "calorias": 350,
      "instrucoes": "Misture tudo e asse por 40 minutos."
  }'
  ```

### Testar com Swagger

Acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para usar a interface interativa de teste.
