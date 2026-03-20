from database.connection import get_connection

SQL_CRIAR_TABELAS = """
CREATE TABLE IF NOT EXISTS Paciente (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            VARCHAR(100) NOT NULL,
    cpf             VARCHAR(14)  NOT NULL UNIQUE,
    data_nascimento DATE         NOT NULL,
    telefone        VARCHAR(20),
    endereco        VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS Medico (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          VARCHAR(100) NOT NULL,
    crm           VARCHAR(20)  NOT NULL UNIQUE,
    especialidade VARCHAR(100),
    telefone      VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS StatusConsulta (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS AgendaMedica (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    medico_id   INTEGER NOT NULL,
    dia_semana  INTEGER NOT NULL,
    hora_inicio TIME    NOT NULL,
    hora_fim    TIME    NOT NULL,
    FOREIGN KEY (medico_id) REFERENCES Medico(id)
);

CREATE TABLE IF NOT EXISTS Consulta (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    medico_id   INTEGER NOT NULL,
    data        DATE    NOT NULL,
    hora        TIME    NOT NULL,
    status_id   INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (paciente_id) REFERENCES Paciente(id),
    FOREIGN KEY (medico_id)   REFERENCES Medico(id),
    FOREIGN KEY (status_id)   REFERENCES StatusConsulta(id)
);
"""

SQL_DADOS_INICIAIS = """
INSERT OR IGNORE INTO StatusConsulta (id, descricao) VALUES (1, 'Agendada');
INSERT OR IGNORE INTO StatusConsulta (id, descricao) VALUES (2, 'Realizada');
INSERT OR IGNORE INTO StatusConsulta (id, descricao) VALUES (3, 'Cancelada');
"""

def inicializar_banco():
    print("[DB] Inicializando banco de dados...")

    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.executescript(SQL_CRIAR_TABELAS)
    cursor.executescript(SQL_DADOS_INICIAIS)

    conexao.commit()

    print("[DB] Tabelas criadas e banco pronto!")

    conexao.close()