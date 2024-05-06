import pyodbc

def conectar():
    try:
        # String de conexão com autenticação do Windows
        conn_str = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=server123;'  # Substitua pelo nome do seu servidor
            'DATABASE=ContosoRetailDW;'
            'Trusted_Connection=yes;'  # Substitua pelo nome do seu banco de dados
        )

        # Conectando ao banco de dados
        conn = pyodbc.connect(conn_str)
        print("Conexão bem-sucedida!")
        return conn

    except Exception as e:
        print("Erro ao conectar ao SQL Server:", e)
        return None

