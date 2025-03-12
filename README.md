# Features para Implementar

# Ideias Futuras
Verificar a necessidade futuramente

## ORM

Implementar um esquema mais fácil para lidar com o banco de dados, dado a grande quantidade de migrations/queries do banco...

# Importantes
# Ping server

Criar testes

# Argumentos Incorretos

Tratar a exceção para quando o subprocess falha por conta dos argumentos...

# Processos por servidor

Separar cada processo por servidor para evitar conflitos

# JSON Processos Agendados

Para facilitar na questão do backup, ou migração dos processos agendados para um novo banco de dados...

# Horário de Agendamento

Na tabela de processos executados utiliza-se o mesmo valor do scheduled_time. Poderíamos utilizar um novo
nome executed_time e inserir somente a data/hora do início da execução...