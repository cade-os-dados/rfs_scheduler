import sqlite3

id_processo = input("Digite o id do processo: ")
query = f'SELECT msg_error FROM executed_processes WHERE id = {id_processo}'

with sqlite3.connect('data/scheduler.db') as conexao:
    cursor = conexao.cursor()
    msg_error = cursor.execute(query).fetchone()

print('\nA seguir está a mensagem de erro do processo: \n\n', msg_error[0])