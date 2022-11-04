import pyodbc
import bot_telegran

# Função de retornar a conexão db

def conexao_sql():
    HOST = "1.1.1.1"  # ou "dominio.com"
    # nome do banco de dados, se você quiser apenas se conectar ao servidor MySQL, deixe-o vazio
    DATABASE = "NomeDataBAse"
    # este é o usuário de acesso ao DB
    USER = "seu_usuario"
    # senha do usuário
    PASSWORD = "seu_senha"
    try:
        string_conexao = 'Driver={SQL Server Native Client 11.0};Server=' + HOST + ';Database=' + DATABASE + ';UID=' + USER + ';PWD=' + PASSWORD
        "user string de conexao abaixo caso o usuario logado na manquisa seja o mesmo com acesso ao DB"
        # string_conexao = 'Driver={SQL Server Native Client 11.0};Server='+HOST+';Database='+DATABASE+';Trusted_Connection=yes;'
        conection = pyodbc.connect(string_conexao)
        return conection.cursor()
    except:
        msg = 'Erro ao conectar ao banco de dados: '
        bot_telegran.send_message(msg=msg)
        return False


# Função de retornar lista de CPFs
def list_cpf():
    cpf_lista = []
    cursor = conexao_sql()
    sql = "SELECT CPF FROM ENVIO_EMAIL;"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        cpf_lista.append(str(row))
        for row in cursor:
            cpf_lista.append(str(row))
    return cpf_lista
