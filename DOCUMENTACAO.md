1. Visão Geral do Sistema

O Hospital System é um sistema acadêmico desenvolvido em Python com o objetivo de simular um sistema interno de gestão de consultas médicas.

O sistmea foi projetado para representar o fluxo básico de trabalho de um secretario hospitalar, permitindo o cadastro de pacientes, médicos e o agendamento de consultas.

O projeto busca aplicar boas práticas de arquitetura de software, organização de código e modelagem de dados.

2. Objetivo do Projeto

Implementar CRUD completo
Metodologia RAD
Desenvolvimento de Interface Gráfica com Tkinter
Arquitetura em Camadas
Compreender modelagem de dados e regras de negócio
Praticar desenvolvimento em Python
Utilizar banco de dados SQLite

3. Tecnologias Utilizadas

Linguagem: Python 3
Interface gráfica: Tkinter + ttk
Banco de Dados: SQLite
Arquitetura: camadas (models, services, repositories)

4. Arquitetura do Sistema

models
repositories
services
interfaces
database

5. Modelo de Dados

Paciente -
| id
| nome
| cpf
| data_nascimento
| telefone
| endereco

Médico -
| id
| nome
| crm
| especialidade
| telefone

Consulta -
| id
| paciente_id
| medico_id
| data
| hora
| status_id

AgendaMedica -
| id
| medico_id
| dia_semana
| hora_inicio
| hora_fim

6. Regras de Negócio

CPF único
CRM único
Médico não pode ter duas consultas em mesmo horário
Uma consulta deve possuir um paciente e um médico
Consultas não podem ser agendadas em datas passadsa

7. Fluxo do Sistema

Login
|
Tela Principal
|
Pacientes
Médicos
Consultas

8. Fluxo de Agendamento

Selecionar Paciente
Selecionar Médico
Escolher data
Escolher horário
Confirmar consulta

9. Metodologia de Desenvolvimento

Rapid Application Development -
| modelagem
| construção rápida
| testes
| ajustes

10. Evoluções Futuras

prontuário médico
histórico de consultas
exportação de relatórios
dashboard de atendimentos