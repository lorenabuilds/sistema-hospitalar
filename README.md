# 🏥 Sistema de Gerenciamento Hospitalar

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Versão](https://img.shields.io/badge/vers%C3%A3o-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

Sistema para gerenciar o dia a dia de um hospital: cadastro de pacientes, agendamento de consultas, prontuário eletrônico, exames, internações, leitos e estoque de medicamentos, com controle de acesso por perfil de usuário.

> Trabalho prático da disciplina **Análise e Projeto de Sistemas**.

<!-- Substitua pelo GIF ou print da aplicação funcionando -->
![Demonstração do sistema](docs/imagens/demo.gif)

---

## 📌 Visão geral

### Problema que o sistema resolve

Em muitos hospitais, informações de pacientes, agendas, prontuários e estoque ficam espalhadas em planilhas, papéis e sistemas que não conversam entre si. Isso causa conflitos de horário, perda de histórico clínico, falta de medicamentos e risco para o paciente, como a prescrição de um remédio ao qual ele é alérgico.

Este sistema centraliza essas informações e aplica as regras de negócio automaticamente, reduzindo erros e agilizando o atendimento.

### Principais funcionalidades

- [ ] Cadastro e consulta de pacientes, com validação de CPF duplicado
- [ ] Autenticação de usuários e controle de acesso por perfil (recepcionista, médico, enfermeiro e administrador)
- [ ] Agendamento, alteração, confirmação e cancelamento de consultas, com bloqueio de conflito de horário
- [ ] Atendimento de emergência, fora das regras de horário comum
- [ ] Prontuário eletrônico com histórico de atendimentos
- [ ] Registro de atendimento e prescrição de medicamentos, com **alerta de alergia**
- [ ] Solicitação de exames e registro de resultados
- [ ] Gerenciamento de leitos e internações, com histórico de transferências
- [ ] Controle de estoque de medicamentos, com lotes, validade e estoque mínimo
- [ ] Verificação de cobertura de convênio antes da confirmação da consulta
- [ ] Relatórios gerenciais e indicadores hospitalares
- [ ] Registro de atividades dos usuários e envio de notificações e alertas

> Marque cada item com `[x]` conforme for sendo implementado.

### Escopo

**O sistema faz:** gestão de pacientes, consultas, prontuários, exames, internações, leitos, estoque de medicamentos, usuários e permissões, relatórios e notificações.

**O sistema não faz:** faturamento financeiro completo, folha de pagamento, telemedicina e integração real com laudos de imagem.

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3.11+ |
| API | FastAPI |
| Banco de dados | SQLite |
| Documentação da API | Swagger UI (gerada automaticamente em `/docs`) |
| Diagramas | draw.io e Mermaid |
| Versionamento | Git e GitHub |

---

## 🚀 Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/<usuario>/sistema-hospitalar.git
cd sistema-hospitalar

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie a aplicação
uvicorn src.main:app --reload
```

Depois, acesse **http://localhost:8000/docs** para testar as funcionalidades pela interface interativa.

> Ajuste os comandos conforme a estrutura final do código.

---

## 📂 Estrutura do repositório

```
sistema-hospitalar/
├── README.md
├── docs/
│   ├── requisitos/
│   ├── diagramas/
│   ├── imagens/
│   └── documentacao.pdf
└── src/
```

---

## 📄 Documentação

- Requisitos funcionais, não funcionais e regras de negócio: `docs/requisitos/`
- Diagrama de casos de uso e diagrama de classes: `docs/diagramas/`
- Documento completo (PDF): `docs/documentacao.pdf`

---

## 🤝 Contribuição e padrão de commits

O projeto usa **Conventional Commits**:

```
feat: adiciona cadastro de paciente
fix: corrige validação de CPF duplicado
docs: adiciona diagrama de classes ao repositório
refactor: separa regras de agendamento em classe própria
test: adiciona testes do agendamento de consultas
chore: configura ambiente do projeto
```

---

## 👩‍💻 Integrantes

| Nome | GitHub |
| --- | --- |
| [Nome da integrante 1] | [@usuario1](https://github.com/usuario1) |
| [Nome da integrante 2] | [@usuario2](https://github.com/usuario2) |

**Disciplina:** Análise e Projeto de Sistemas
**Data:** novembro de 2026

---

## 📜 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais informações.