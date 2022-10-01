CREATE TABLE IF NOT EXISTS aluno (
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    data_nascimento INTEGER NOT NULL,
    CONSTRAINT Aluno_PK PRIMARY KEY (email),
    CHECK (
        typeof("nome") = "text"
        AND length("nome") <= 100
        AND typeof("email") = "text"
        AND length("email") <= 50
        AND "email" LIKE "%@%.%"
    )
);
CREATE TABLE IF NOT EXISTS disciplina (
    nome TEXT NOT NULL,
    carga_horaria INTEGER NOT NULL,
    pk INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT CHECK (
        typeof("nome") = "text"
        AND length("nome") <= 100
        AND typeof("carga_horaria") = "integer"
        AND length("carga_horaria") <= 4
        AND "carga_horaria" >= 0
    )
);
CREATE TABLE IF NOT EXISTS boletim (
    data_entrega INTEGER,
    aluno TEXT NOT NULL,
    CONSTRAINT Boletim_FK FOREIGN KEY (aluno) REFERENCES Aluno(email),
    UNIQUE(data_entrega, aluno) pk INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE IF NOT EXISTS notas_boletim (
    disciplina TEXT NOT NULL,
    boletim INTEGER NOT NULL,
    nota INTEGER NOT NULL,
    pk INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    CHECK (
        typeof("nota") = "integer"
        AND length("nota") <= 3
        AND "nota" >= 0
    )
);