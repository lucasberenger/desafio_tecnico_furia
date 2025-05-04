# 🤖 Desafio Técnico da Vaga de Assistente de Engenharia de Software da FURIA Tech

Este projeto foi desenvolvido como parte do **desafio técnico da FURIA**, com o objetivo de integrar os dois desafios propostos em um único sistema.

A ideia é entregar benefícios exclusivos para os torcedores da FURIA, mas para isso, eles devem se cadastrar como sócios do clube, assim como é feito no futebol brasileiro. O chatbot, nesse caso, seria apenas um dos benefícios de ser sócio-torcedor da FURIA.

Para se tornar um sócio, o torcedor deve conceder algumas informações pessoais, incluindo redes socias, o que servirá para a análise de dados.

---

## 🚀 Tecnologias Utilizadas

### Backend

- **[FastAPI](https://fastapi.tiangolo.com/)** — Framework web moderno e rápido para APIs em Python.
- **[Redis](https://redis.io/)** — Armazenamento em memória para dados do bot.
- **SQLite** — Banco de dados leve e local para persistência.
- **[Docker](https://www.docker.com/)** — Containerização para ambiente de desenvolvimento e deploy.

### Chatbot

- **[RapidFuzz](https://maxbachmann.github.io/RapidFuzz/)** — Biblioteca de fuzzy matching para interpretar perguntas dos usuários.

### Scraping

- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** — Para extrair informações de páginas HTML.
- **[Selenium](https://www.selenium.dev/)** — Para automação de navegação e coleta dinâmica de conteúdo.

### Front-end

- **[Tailwind CSS](https://tailwindcss.com/)** — Framework de estilos utilitário para construir rapidamente a interface.
- **[Jinja2](https://jinja.palletsprojects.com/)** — Motor de templates para renderização HTML.

---

## 💡 Funcionalidades

- Scraping automatizado de dados com Selenium e BeautifulSoup.
- Armazenamento dos dados estruturados no Redis.
- Respostas inteligentes via RapidFuzz.
- API com FastAPI para comunicação com o front-end.
- Interface responsiva usando Tailwind e Jinja2.

---

## 📦 Como Executar o Projeto

### Pré-requisitos

- Necessário Docker e Docker Compose.

### Passos

1. **Clone o repositório:**

```bash
git clone https://github.com/lucasberenger/desafio_tecnico_furia.git
cd desafio_tecnico_furia
```

2. **Execute o compose para subir os containers**

```bash
docker compose up --build -d
```

3. **Acesse a aplicação**

Acesse em http://localhost:8000

## 📄 Licença

Este projeto está licenciado sob os termos da Licença MIT.

## 📫 Contato

Lucas Berenger

envtux@gmail.com

v1.0.0
