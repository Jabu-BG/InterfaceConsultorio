import sqlite3
import os

conexao = sqlite3.connect("hospital.bd")
cursor = conexao.cursor()

cursor.execute("INSERT INTO Paciente (nome, cpf, nascimento, telefone, endereco) VALUES ('Victor', 7174231923, '22-07-2006', 21992342324, 'Viaduto Dultra')")

cursor.execute("INSERT INTO Paciente (nome, cpf, nascimento, telefone, endereco) VALUES ('Borges', 199234512, '26-03-2006', 21992562562, 'Clito de Araujogit')")


conexao.commit()

conexao.close()
