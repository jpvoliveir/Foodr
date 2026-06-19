# ML Food Recommender API

Esta é uma API desenvolvida com **FastAPI** para calcular metas calóricas/macronutrientes (TMB e GETD) e fornecer recomendações de alimentos com base no perfil físico e objetivos do usuário, utilizando o algoritmo **Cosine Similarity** (Similaridade de Cosseno) da biblioteca `scikit-learn`.

---

## 🚀 Como Executar

### Opção 1: Executando Localmente

1. **Ative o ambiente virtual:**
   ```powershell
   & ".\.venv\Scripts\Activate.ps1"
   ```
2. **Inicie o servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```
3. A API estará disponível em: `http://127.0.0.1:8000`
4. Documentação Swagger interativa: `http://127.0.0.1:8000/docs`

### Opção 2: Executando com Docker

1. **Construa e inicie os contêineres:**
   ```bash
   docker compose up --build
   ```
2. A API estará disponível no mesmo endereço `http://127.0.0.1:8000`.

---

## 📁 Estrutura do Projeto

```text
food-recommender/
├── app/
│   ├── main.py                   # Ponto de entrada e carregamento dos dados
│   ├── database.py               # Configurações de conexão do SQLite e SQLAlchemy
│   ├── models/
│   │   ├── user.py               # Modelo e schemas Pydantic do Usuário
│   │   └── food.py               # Modelo e schemas Pydantic dos Alimentos
│   ├── routes/
│   │   ├── users.py              # Endpoints para gerenciamento do perfil do usuário
│   │   └── recommendations.py    # Endpoints de recomendação inteligente
│   └── services/
│       ├── metabolism.py         # Cálculos de BMR/TDEE e metas de macronutrientes
│       └── recommender.py        # Algoritmo de Similaridade de Cosseno com Scikit-Learn
├── data/
│   └── foods.csv                 # Banco de dados inicial de alimentos
├── dockerfile                    # Arquivo Dockerfile para a API
├── docker-compose.yml            # Orquestração do Docker Compose
├── requirements.txt              # Dependências do Python
└── README.md                     # Documentação do projeto
```

---

## 🧪 Endpoints Principais

### Usuários (`/users`)
- `POST /users/` - Cria um perfil de usuário e calcula a ingestão necessária de água e metas nutricionais.
- `GET /users/{user_id}` - Retorna o perfil do usuário e suas metas metabólicas calculadas.
- `PUT /users/{user_id}` - Atualiza os dados físicos ou metas do usuário.

### Recomendações (`/recommendations`)
- `GET /recommendations/{user_id}` - Fornece uma lista de alimentos ordenados por similaridade de acordo com a necessidade metabólica daquele usuário.
- `GET /recommendations/direct/run` - Permite calcular metas e obter recomendações de forma instantânea sem precisar salvar um perfil no banco de dados.

---

## 🧠 Como funciona a Recomendação com Machine Learning?

1. **Cálculo de Ingestão de Calorias & Macros (Mifflin-St Jeor)**:
   - O aplicativo calcula a Taxa Metabólica Basal (BMR) e o Gasto Energético Diário Total (TDEE) com base no peso, altura, idade, sexo e nível de atividade física do usuário.
   - O objetivo (perda, ganho ou manutenção de peso) define as metas diárias de calorias.
   - Os alvos de macronutrientes (Proteínas, Carboidratos e Gorduras) são distribuídos para atingir essas metas (ex: 2.0g/kg de proteína, 25% gordura e o restante em carboidratos).

2. **Vetorização e Similaridade de Cosseno**:
   - O perfil ideal de macronutrientes do usuário é normalizado para um vetor de proporção de 3 dimensões: `[Proporção de Proteína, Proporção de Carboidrato, Proporção de Gordura]`.
   - Cada alimento do banco de dados (ex: arroz, frango, abacate) é representado da mesma forma.
   - A biblioteca `scikit-learn` calcula a **Similaridade de Cosseno** entre o vetor de metas do usuário e os vetores de cada alimento do banco de dados. Os alimentos com proporções nutricionais mais próximas da proporção de alvos ideal do usuário ganham as pontuações mais altas (mais próximas de `1.0`).
   - Os resultados são filtrados para seguir preferências alimentares (como veganismo/vegetarianismo) antes de serem retornados.
