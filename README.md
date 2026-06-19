# 🍎 Foodr

Foodr é uma API de recomendação de alimentos desenvolvida com FastAPI e Docker. O sistema utiliza informações físicas do usuário para calcular necessidades energéticas diárias, metas de macronutrientes e recomendar alimentos compatíveis com seus objetivos nutricionais.

As recomendações são geradas utilizando Similaridade de Cosseno (Cosine Similarity) através da biblioteca Scikit-Learn, comparando o perfil nutricional ideal do usuário com os alimentos disponíveis na base de dados.

---

## 🚀 Funcionalidades

* Cadastro de usuários
* Cálculo de Taxa Metabólica Basal (TMB)
* Cálculo de Gasto Energético Diário Total (GETD)
* Definição automática de metas nutricionais
* Recomendação personalizada de alimentos
* Filtro por preferências alimentares
* Documentação automática com Swagger UI
* Containerização com Docker

---

## 🛠 Tecnologias Utilizadas

* Python 3
* FastAPI
* SQLAlchemy
* SQLite
* Pandas
* Scikit-Learn
* Docker
* Docker Compose

---

## 🚀 Como Executar

### Executando Localmente

1. Ative o ambiente virtual:

```powershell
& ".\.venv\Scripts\Activate.ps1"
```

2. Inicie o servidor:

```bash
uvicorn app.main:app --reload
```

3. Acesse:

```text
http://127.0.0.1:8000
```

Documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

---

### Executando com Docker

```bash
docker compose up --build
```

Após iniciar os containers:

```text
http://127.0.0.1:8000/docs
```

---

## 📁 Estrutura do Projeto

```text
foodr/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── user.py
│   │   └── food.py
│   ├── routes/
│   │   ├── users.py
│   │   └── recommendations.py
│   └── services/
│       ├── metabolism.py
│       └── recommender.py
├── data/
│   └── foods.csv
├── dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧪 Principais Endpoints

### Usuários

| Método | Endpoint           | Descrição                 |
| ------ | ------------------ | ------------------------- |
| POST   | `/users/`          | Cria um usuário           |
| GET    | `/users/{user_id}` | Retorna dados do usuário  |
| PUT    | `/users/{user_id}` | Atualiza dados do usuário |

### Recomendações

| Método | Endpoint                      | Descrição                             |
| ------ | ----------------------------- | ------------------------------------- |
| GET    | `/recommendations/{user_id}`  | Retorna recomendações personalizadas  |
| GET    | `/recommendations/direct/run` | Gera recomendações sem salvar usuário |

---

## 🧠 Modelo de Recomendação

O sistema utiliza uma abordagem baseada em conteúdo (*Content-Based Filtering*).

### Etapa 1 — Cálculo Metabólico

Com base em:

* Peso
* Altura
* Idade
* Sexo
* Nível de atividade física
* Objetivo nutricional

o sistema calcula:

* Taxa Metabólica Basal (TMB)
* Gasto Energético Diário Total (GETD)
* Meta diária de calorias
* Distribuição de proteínas, carboidratos e gorduras

### Etapa 2 — Similaridade de Cosseno

O perfil nutricional ideal do usuário é transformado em um vetor de macronutrientes:

```text
[Proteína, Carboidrato, Gordura]
```

Cada alimento é representado da mesma forma.

Utilizando o algoritmo Cosine Similarity do Scikit-Learn, o sistema mede a proximidade entre os vetores e retorna os alimentos mais compatíveis com as metas nutricionais do usuário.

---

## 📖 Documentação

Após iniciar a aplicação, a documentação interativa estará disponível em:

```text
http://127.0.0.1:8000/docs
```
