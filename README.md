# StudyFlow

Aplicativo de produtividade acadêmica desenvolvido com **Python + Flet**, com persistência de dados em **SQLite**. Projeto desenvolvido ao longo de 8 semanas para a disciplina de Tecnologia da Informação — IFSC Câmpus Lages.

---

## Funcionalidades

| Tela | O que faz |
|---|---|
| **Dashboard** | Visão geral com métricas de tarefas, barra de progresso e lista de recentes |
| **Tarefas** | CRUD de tarefas com prioridade (Alta/Média/Baixa), filtro e seleção de data |
| **Pomodoro** | Timer de foco configurável com ciclos automáticos de pausa curta e longa |
| **Anotações** | Registro de conteúdo por matéria com título e texto |
| **Cronograma** | Grade semanal com slots de estudo por dia da semana |
| **Usuário** | Identificação por nome e e-mail com persistência entre sessões |
| **Configurações** | Alternância entre tema claro e escuro |
| **Sobre** | Histórico de desenvolvimento do projeto |

---

## Tecnologias

- **Python 3.10+**
- **Flet 0.85.1** — framework para interfaces gráficas em Python
- **SQLite 3** — banco de dados relacional embutido (sem instalação adicional)

---

## Estrutura do projeto

```
studyflow/
│
├── main.py                  # Ponto de entrada; inicializa banco e monta o app
├── requirements.txt         # Dependências do projeto
│
├── components/
│   ├── header.py            # Componente de cabeçalho reutilizável
│   └── menu.py              # Menu lateral de navegação
│
├── database/
│   ├── db.py                # Conexão SQLite e criação automática das tabelas
│   ├── usuarios.py          # criar_usuario, autenticar, buscar_por_id
│   ├── tarefas.py           # adicionar, listar, concluir, excluir, excluir_todas
│   ├── anotacoes.py         # adicionar, listar, atualizar, excluir
│   └── cronograma.py        # adicionar, listar, excluir
│
├── views/
│   ├── home.py              # Dashboard
│   ├── tarefas.py           # Gerenciamento de tarefas
│   ├── pomodoro.py          # Timer Pomodoro
│   ├── anotacoes.py         # Anotações por matéria
│   ├── cronograma.py        # Grade semanal
│   ├── usuario.py           # Login / identificação
│   ├── config.py            # Configurações de aparência
│   └── sobre.py             # Informações do projeto
│
└── theme/
    └── paleta.py            # Paletas de cores claro/escuro e componente criar_card
```

---

## Banco de dados

O arquivo `studyflow.db` é gerado automaticamente na primeira execução e **não faz parte do repositório**. As tabelas são:

```
usuarios      (id, nome, email, senha)
configuracoes (id, usuario_id)
tarefas       (id, usuario_id, nome, prioridade, concluida)
anotacoes     (id, usuario_id, titulo, conteudo)
cronograma    (id, usuario_id, disciplina, data, horario)
```

Todos os dados são isolados por usuário via `usuario_id`.

---

## Como executar

**1. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**2. Execute o app:**

```bash
python main.py
```

**3. Primeiro acesso:**

Vá em **Usuário** no menu lateral, insira seu nome e e-mail e clique em **Entrar**. O cadastro é criado automaticamente se o e-mail ainda não existir no banco.

> Os dados persistem entre sessões — fechar e reabrir o app mantém tarefas, anotações e cronograma.

---

## Progressão de desenvolvimento

| Semana | Conteúdo |
|---|---|
| 1 | Tela única: texto + botão |
| 2 | Campos e interatividade real |
| 3 | Row, Column, Container |
| 4 | Menu lateral com navegação visual |
| 5 | Navegação real com rotas |
| 6 | AppBar, ícones e SnackBar |
| 7 | Componentização e código escalável |
| 8 | Dark mode, banco de dados SQLite e produto final |

---
