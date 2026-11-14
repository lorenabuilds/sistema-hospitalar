# Requisitos do Sistema de Gerenciamento Hospitalar

## 1. Requisitos Funcionais (RF)

### RF.01 — Cadastrar pacientes
O sistema deve permitir cadastrar, consultar e atualizar as informações dos pacientes apenas por profissionais de saúde autorizados, incluindo nome completo, informações pessoais, dados de contato, endereço, contato de emergência, alergias e demais informações necessárias para sua identificação e atendimento.

### RF.02 — Gerenciar usuários e profissionais
O sistema deve permitir cadastrar, consultar, atualizar, ativar e desativar os usuários que terão acesso ao sistema, mantendo suas informações e funções dentro da instituição. O sistema também deve permitir o cadastro e gerenciamento dos profissionais que atuam no hospital, armazenando informações como dados pessoais, função, especialidade, registro profissional, setor de atuação e situação no sistema.

### RF.03 — Controlar permissões de acesso
O sistema deve permitir controlar as permissões de acesso dos usuários de acordo com seus respectivos perfis e funções, garantindo que cada usuário possa acessar somente as funcionalidades e informações autorizadas.

### RF.04 — Gerenciar consultas
O sistema deve permitir consultar, agendar, confirmar, alterar e cancelar consultas de acordo com os níveis de acesso dos usuários, considerando a disponibilidade dos profissionais e os horários de atendimento. O agendamento de consultas deve ocorrer dentro do horário de atendimento clínico, das 07:00 às 18:00, exceto para atendimentos de emergência.

### RF.05 — Gerenciar prontuários eletrônicos
O sistema deve permitir que profissionais de saúde autorizados cadastrem, consultem, registrem e atualizem o prontuário eletrônico dos pacientes, mantendo centralizadas informações como histórico de atendimentos, medicamentos prescritos, exames, procedimentos e evoluções clínicas.

### RF.06 — Gerenciar leitos
O sistema deve permitir cadastrar e acompanhar os leitos disponíveis, ocupados, reservados ou em manutenção, possibilitando o controle de sua localização, setor e situação atual dentro da instituição.

### RF.07 — Gerenciar internações
O sistema deve permitir registrar e acompanhar as internações dos pacientes, incluindo admissão, permanência, transferência entre setores e alta hospitalar, mantendo o histórico da internação associado ao prontuário do paciente.

### RF.08 — Solicitar exames e registrar resultados
O sistema deve permitir que profissionais de saúde autorizados solicitem exames para os pacientes e que os resultados sejam posteriormente registrados e disponibilizados no prontuário eletrônico, permitindo acompanhar o status dos exames desde sua solicitação até a disponibilização dos resultados.

### RF.09 — Gerar relatórios
O sistema deve permitir gerar relatórios relacionados às atividades hospitalares, possibilitando a consulta e análise de informações sobre pacientes, consultas, internações, exames, medicamentos, estoque, profissionais e demais dados administrativos.

### RF.10 — Gerenciar estoque e medicamentos
O sistema deve permitir cadastrar, consultar e controlar medicamentos e materiais hospitalares, possibilitando o gerenciamento de entradas e saídas, lotes, quantidades disponíveis, datas de validade, fornecedores e dispensações. O sistema também deve permitir acompanhar a movimentação dos itens disponíveis e identificar materiais e medicamentos em falta no hospital.

### RF.11 — Exibir indicadores hospitalares
O sistema deve exibir indicadores para acompanhamento do funcionamento da instituição, como quantidade de atendimentos, taxa de ocupação de leitos, número de internações, altas, consultas realizadas, exames realizados e demais informações relevantes para a gestão hospitalar.

### RF.12 — Registrar atividades dos usuários
O sistema deve registrar as principais atividades realizadas pelos usuários, permitindo identificar as ações executadas, alterações realizadas, data, horário e informações relacionadas ao acesso e à utilização do sistema.

### RF.13 — Enviar notificações e alertas
O sistema deve permitir o envio de notificações e alertas relacionados às atividades hospitalares, como consultas agendadas, resultados de exames disponíveis, alterações de status, estoque baixo de materiais e medicamentos, medicamentos próximos do vencimento e outras situações relevantes.

### RF.14 — Registrar atendimentos e prescrever medicamentos
O sistema deve permitir que médicos registrem o atendimento realizado ao paciente e prescrevam medicamentos, vinculando as informações ao prontuário eletrônico. Ao prescrever, o sistema deve emitir um alerta caso o medicamento seja incompatível com as alergias registradas do paciente.

### RF.15 — Verificar cobertura de convênio
O sistema deve permitir registrar o convênio do paciente e verificar a cobertura do atendimento junto ao sistema de convênio antes da confirmação da consulta.

---

## 2. Requisitos Não Funcionais (RNF)

### RNF.01 — Segurança
O sistema deve garantir a proteção das informações armazenadas, impedindo acessos não autorizados e permitindo que cada usuário tenha acesso apenas aos recursos e dados correspondentes às suas permissões. As informações sensíveis devem ser protegidas durante seu armazenamento e transmissão.

**Critérios de verificação:**
- Senhas armazenadas com algoritmo de hash seguro (por exemplo, bcrypt), nunca em texto puro.
- Toda comunicação realizada por HTTPS (TLS 1.2 ou superior).
- Em 100% dos testes, a tentativa de acessar um recurso sem permissão deve ser negada.
- A sessão deve expirar após 30 minutos de inatividade.

### RNF.02 — Disponibilidade
O sistema deve permanecer disponível durante o período de funcionamento do hospital, permitindo que os profissionais acessem as informações necessárias para realizar suas atividades. O sistema deve possuir mecanismos que reduzam o impacto de falhas e indisponibilidades.

**Critérios de verificação:**
- Disponibilidade mínima de 99% por mês durante o horário de funcionamento do hospital.
- Backup completo dos dados realizado diariamente.
- Restauração do sistema a partir do backup em até 4 horas após uma falha.

### RNF.03 — Desempenho
O sistema deve apresentar respostas rápidas durante a execução das operações, como consultas de pacientes, acesso a prontuários, agendamentos e pesquisas. O tempo de resposta deve permanecer adequado mesmo com o aumento da quantidade de informações armazenadas.

**Critérios de verificação:**
- Em 95% das requisições, consultas de pacientes, prontuários e agenda respondem em até 2 segundos, com até 10.000 pacientes cadastrados e 50 usuários simultâneos.
- Relatórios gerenciais são gerados em até 10 segundos.

### RNF.04 — Escalabilidade
O sistema deve ser desenvolvido de forma que possa suportar o crescimento da quantidade de pacientes, usuários, atendimentos e informações armazenadas sem comprometer significativamente seu funcionamento e desempenho.

**Critérios de verificação:**
- Suportar até 100.000 pacientes cadastrados e 200 usuários simultâneos, com aumento de no máximo 20% no tempo de resposta definido no RNF.03.

### RNF.05 — Usabilidade
O sistema deve possuir uma interface simples, clara e intuitiva, permitindo que os diferentes usuários realizem suas atividades com facilidade. As funcionalidades e informações devem ser apresentadas de maneira organizada, reduzindo a possibilidade de erros durante a utilização.

**Critérios de verificação:**
- Um recepcionista deve conseguir cadastrar um paciente em até 3 minutos, sem treinamento prévio, em pelo menos 90% dos testes de usabilidade.
- As funcionalidades principais devem estar a no máximo 3 cliques do menu inicial.
- Mensagens de erro devem indicar qual campo precisa ser corrigido.

### RNF.06 — Acessibilidade
O sistema deve seguir boas práticas de acessibilidade, permitindo que pessoas com diferentes necessidades possam utilizar suas funcionalidades. A interface deve considerar aspectos como contraste, navegação, identificação de elementos e compatibilidade com tecnologias assistivas.

**Critérios de verificação:**
- Conformidade com as diretrizes WCAG 2.1, nível AA.
- Contraste mínimo de 4,5:1 entre texto e fundo.
- Todas as funcionalidades principais devem ser acessíveis apenas pelo teclado.
- Elementos da interface devem possuir rótulos compatíveis com leitores de tela.

### RNF.07 — Privacidade
O sistema deve garantir o tratamento adequado das informações pessoais e dos dados relacionados à saúde dos pacientes, seguindo os princípios e requisitos aplicáveis da Lei Geral de Proteção de Dados (LGPD). O acesso e tratamento dessas informações devem ocorrer de maneira controlada e segura.

**Critérios de verificação:**
- 100% dos acessos a prontuários devem ser registrados em log, com usuário, data e horário.
- Dados pessoais só devem ser exibidos a perfis autorizados, inclusive em relatórios.
- O sistema deve coletar apenas os dados necessários ao atendimento.

### RNF.08 — Manutenibilidade
O sistema deve possuir uma arquitetura organizada e um código estruturado de forma modular, facilitando a identificação de problemas, correções, atualizações e inclusão de novas funcionalidades sem comprometer as funcionalidades existentes.

**Critérios de verificação:**
- Código organizado em módulos separados por funcionalidade (por exemplo, pacientes, consultas, prontuários).
- Testes automatizados cobrindo pelo menos 60% das regras de negócio principais.
- Um novo módulo deve poder ser adicionado sem alterar o código dos módulos existentes.

### RNF.09 — Auditoria
O sistema deve registrar operações relevantes realizadas pelos usuários, permitindo identificar as ações realizadas, os usuários responsáveis, as datas e os horários. Os registros devem possibilitar o acompanhamento e a rastreabilidade das alterações realizadas nas informações do sistema.

**Critérios de verificação:**
- 100% das operações de criação, alteração e inativação de registros devem gerar log com usuário, ação, data e horário.
- Os logs não podem ser alterados ou excluídos por usuários comuns.
- Os logs devem ser mantidos por, no mínimo, 12 meses.

---

## 3. Regras de Negócio (RN)

### RN.01 — Acesso ao sistema
O acesso ao sistema deve ser realizado mediante autenticação, sendo permitido somente a usuários previamente cadastrados e ativos.

### RN.02 — Controle de acesso
Cada usuário deve possuir permissões de acordo com seu perfil e função, podendo acessar somente as funcionalidades e informações autorizadas.

### RN.03 — Cadastro de pacientes
O cadastro de um paciente deve possuir as informações necessárias para sua identificação e atendimento, não sendo permitido o registro de pacientes sem os dados obrigatórios definidos pelo sistema.

### RN.04 — Atualização de dados do paciente
Alterações nas informações dos pacientes devem ser realizadas somente por usuários autorizados e devem ser registradas para fins de rastreabilidade.

### RN.05 — Agendamento de consultas
As consultas devem ser agendadas somente dentro do horário de atendimento clínico estabelecido pelo hospital, das 07:00 às 18:00, respeitando a disponibilidade do profissional. Atendimentos de emergência não estão sujeitos a essa restrição de horário.

### RN.06 — Conflito de horários
O sistema não deve permitir o agendamento de duas consultas para o mesmo profissional no mesmo horário.

### RN.07 — Cancelamento de consultas
Uma consulta cancelada não deve permanecer disponível como atendimento confirmado e seu histórico deve ser mantido no sistema.

### RN.08 — Prontuário eletrônico
Cada paciente deve possuir um prontuário eletrônico único, no qual devem ser armazenadas suas informações clínicas e seu histórico de atendimento.

### RN.09 — Acesso ao prontuário
O acesso às informações do prontuário deve ser restrito aos profissionais autorizados de acordo com suas funções e permissões.

### RN.10 — Integridade do prontuário
Informações clínicas registradas no prontuário não devem ser excluídas de forma que comprometa seu histórico. Alterações relevantes devem permanecer registradas para fins de auditoria.

### RN.11 — Ocupação de leitos
Um leito não pode ser atribuído simultaneamente a mais de um paciente.

### RN.12 — Status dos leitos
Cada leito deve possuir um status que indique sua situação atual, como disponível, ocupado, reservado ou em manutenção.

### RN.13 — Internação
A internação de um paciente deve estar vinculada ao seu cadastro e prontuário, permitindo acompanhar sua permanência durante o período hospitalar.

### RN.14 — Transferência de paciente
A transferência de um paciente entre setores deve atualizar sua localização e manter o histórico da movimentação no sistema.

### RN.15 — Alta hospitalar
A alta hospitalar deve encerrar a internação ativa do paciente e liberar o leito anteriormente ocupado, quando aplicável.

### RN.16 — Solicitação de exames
Somente profissionais de saúde autorizados podem solicitar exames para os pacientes.

### RN.17 — Resultado de exames
Os resultados dos exames devem ser associados ao paciente e disponibilizados em seu prontuário após o devido registro e validação, quando aplicável.

### RN.18 — Estoque e medicamentos
Toda entrada e saída de medicamentos e materiais hospitalares deve ser registrada no sistema, permitindo acompanhar a quantidade disponível.

### RN.19 — Validade dos medicamentos
Medicamentos com validade expirada não devem ser disponibilizados para dispensação.

### RN.20 — Estoque mínimo
O sistema deve identificar itens que estejam abaixo da quantidade mínima estabelecida e gerar um alerta para os responsáveis.

### RN.21 — Relatórios
O acesso aos relatórios deve respeitar as permissões do usuário e as informações disponibilizadas para seu perfil.

### RN.22 — Indicadores hospitalares
Os indicadores apresentados pelo sistema devem ser calculados com base nas informações registradas nos módulos hospitalares.

### RN.23 — Registro de atividades
As operações relevantes realizadas pelos usuários devem possuir registro contendo, no mínimo, o usuário responsável, a ação realizada, a data e o horário.

### RN.24 — Notificações e alertas
O sistema deve gerar notificações e alertas de acordo com as situações configuradas, como consultas agendadas, resultados disponíveis, estoque baixo e medicamentos próximos do vencimento.

### RN.25 — Privacidade das informações
As informações pessoais e de saúde dos pacientes devem ser acessadas e utilizadas somente para finalidades autorizadas, respeitando as políticas de segurança e privacidade da instituição e a legislação aplicável.

### RN.26 — Alerta de alergia
Ao prescrever um medicamento, o sistema deve verificar as alergias registradas no cadastro do paciente e alertar o profissional em caso de incompatibilidade.

### RN.27 — Confirmação de consulta
Uma consulta agendada deve ser confirmada antes do atendimento, e somente consultas confirmadas podem ser registradas como realizadas.

### RN.28 — Cobertura do convênio
A verificação de cobertura deve ser realizada para pacientes com convênio ativo antes da confirmação da consulta.