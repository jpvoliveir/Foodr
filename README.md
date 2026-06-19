# Foodr
Sistema de recomendação de alimentos desenvolvido com FastAPI e Docker. O projeto utiliza cálculo metabólico basal, metas nutricionais e preferências do usuário para sugerir alimentos e gerar recomendações personalizadas que evoluem com o feedback recebido.

# 🍎 Foodr

Foodr é um sistema de recomendação de alimentos desenvolvido com FastAPI e Docker. O projeto utiliza dados nutricionais, preferências alimentares e metas calóricas para sugerir alimentos personalizados aos usuários.

Inspirado em mecanismos de matching, o sistema aprende continuamente com as avaliações dos usuários para gerar recomendações cada vez mais relevantes.

---

## 🚀 Funcionalidades

- Cadastro de usuários
- Cadastro de alimentos
- Cálculo de Taxa Metabólica Basal (TMB)
- Definição de metas nutricionais
- Recomendação personalizada de alimentos
- Registro de preferências alimentares
- Atualização das recomendações com base no feedback do usuário
- Documentação automática com Swagger UI

---

## 🏗️ Arquitetura

```text
Foodr
│
├── FastAPI
├── Sistema de Recomendação
├── Docker
├── SQLite
└── Swagger UI
