# 🏥 Sistema de Gerenciamento Hospitalar

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Versão](https://img.shields.io/badge/vers%C3%A3o-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

Sistema para gerenciar o dia a dia de um hospital: cadastro de pacientes, agendamento de consultas, prescrições com alerta de alergia, leitos e internações, com controle de acesso por perfil de usuário.

> Trabalho prático da disciplina **Análise e Projeto de Sistemas**.

---

## 📌 Visão geral

### Problema que o sistema resolve

Em muitos hospitais, informações de pacientes, agendas e prontuários ficam espalhadas em planilhas, papéis e sistemas que não conversam entre si. Isso causa conflitos de horário, perda de histórico clínico e risco para o paciente, como a prescrição de um remédio ao qual ele é alérgico.

Este sistema centraliza essas informações e aplica as regras de negócio automaticamente, reduzindo erros e agilizando o atendimento.

### Funcionalidades implementadas

- [x] Cadastro e listagem de pacientes (nome, telefone e alergias)
- [x] Cadastro de usuários com perfis (administrador, médico, enfermeiro e recepcionista)
- [x] Autenticação por login e senha, com menus distintos por perfil
- [x] Agendamento de consultas com validação de horário (07:00–18:00) e bloqueio de conflito
- [x] Listagem e cancelamento de consultas (histórico mantido)
- [x] Prescrição de medicamentos com **alerta de alergia** (prescrição bloqueada em caso de incompatibilidade)
- [x] Cadastro e listagem de leitos
- [x] Internação de pacientes em leitos disponíveis
- [x] Alta hospitalar com liberação do leito

### Funcionalidades previstas (ainda não implementadas)

- [ ] Prontuário eletrônico completo
- [ ] Solicitação de exames e registro de resultados
- [ ] Transferência de pacientes entre setores
- [ ] Controle de estoque de medicamentos (lotes, validade, estoque mínimo)
- [ ] Verificação de cobertura de convênio
- [ ] Relatórios gerenciais e indicadores hospitalares
- [ ] Registro de atividades (log de auditoria)
- [ ] Notificações e alertas automáticos
- [ ] Atendimento de emergência (fora do horário comum)

> Marque cada item com `[x]` conforme for sendo implementado.

### Escopo

**O sistema faz (implementado):** cadastro de pacientes, autenticação por perfil, agendamento e cancelamento de consultas, prescrição com alerta de alergia, cadastro de leitos, internação e alta.

**O sistema não faz:** faturamento financeiro, folha de pagamento, telemedicina, armazenamento de imagens de exames e integração real com sistemas de convênio.

---

## 🛠️ Tecnologias

| Finalidade | Tecnologia |
| --- | --- |
| Linguagem | **Python 3.9+** (puro, sem bibliotecas ou frameworks externos) |
| Diagramas (casos de uso) | draw.io |
| Controle de versão | Git |
| Hospedagem do repositório | GitHub |

> O projeto foi desenvolvido utilizando apenas recursos nativos da linguagem Python, sem dependências externas.

---

## 🚀 Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/lorenabuilds/sistema-hospitalar.git
cd sistema-hospitalar

# 2. Execute a aplicação
python "src/Sistema Hospitalar.py"
```

> Certifique-se de ter o **Python 3.9 ou superior** instalado. Não é necessário instalar bibliotecas adicionais.

### Primeiro acesso

Na primeira execução, o sistema solicita o cadastro do **primeiro usuário**, que será automaticamente definido como **administrador**. A partir daí, o login é feito com login e senha cadastrados.

### Perfis e menus

| Perfil | Opções disponíveis |
| --- | --- |
| **Administrador** | Cadastrar/listar usuários; cadastrar/listar leitos |
| **Recepcionista** | Cadastrar/listar pacientes; agendar/listar/cancelar consultas |
| **Médico** | Listar pacientes e consultas; agendar consulta; prescrever medicamentos; listar prescrições |
| **Enfermeiro** | Listar pacientes e leitos; internar paciente; dar alta |

---

## 📂 Estrutura do repositório

```
sistema-hospitalar/
├── docs/
│   ├── diagramas/
│   ├── documentacao.pdf/
│   └── requisitos/
└── src/
    ├── README.md
    └── Sistema Hospitalar.py
```

---

## 📄 Documentação

- Documento completo (PDF/DOCX): `docs/documentacao.pdf`
- Diagrama de casos de uso: `docs/diagramas/`
- Requisitos funcionais, não funcionais e regras de negócio: `docs/requisitos/`

> O documento de análise e projeto descreve o sistema completo (RF.01–RF.15, RNF.01–RNF.09, RN.01–RN.30). A implementação atual cobre um subconjunto desses requisitos, conforme listado na seção de funcionalidades.

---

## 🤝 Contribuição e padrão de commits

O projeto usa **Conventional Commits**:

```
feat: adiciona cadastro de paciente
docs: adiciona diagrama de casos de uso ao repositório
chore: configura ambiente do projeto
refactor: separa regras de agendamento em função própria
```

---

## 👩‍💻 Integrantes

| Nome | GitHub |
| --- | --- |
| Lorena A. S. de Almeida | [@lorenabuilds](https://github.com/lorenabuilds) |
| Débora Cristina Silva Melo | [@deborac-smelo](https://github.com/deborac-smelo) |

**Disciplina:** Análise e Projeto de Sistemas
**Data:** novembro de 2026

---

## 🔗 Repositório

[github.com/lorenabuilds/sistema-hospitalar](https://github.com/lorenabuilds/sistema-hospitalar)

---

## 📜 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais informações.