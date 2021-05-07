import sqlite3

class Sqlite(object):

    conexao = any

    def __init__(self,dados, banco):
        # Inicializa banco
        conexao = sqlite3.connect('fundos.db')
        conexao.cursor()
       
        if conexao is not None:
            conexao.execute(""" CREATE TABLE IF NOT EXISTS fiis (
                                            id integer NOT NULL PRIMARY KEY,
                                            nomefundo text NOT NULL                                        
                                        ); """)
            conexao.commit()
            # Cria registros do fundo
            conexao.execute("INSERT INTO fiis(nomefundo) VALUES (?)", [dados])                
            conexao.commit()
        else:
            print("Nao conectou no banco.")

        # print('Dados inseridos com sucesso.')
        conexao.close()

    

    





