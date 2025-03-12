# Working on

## Recurrent Processes

Adicionar os processos no banco de dados e fazer o scheduler rodar somente estes processos. Eles devem
estar em uma tabela separada.

Podemos criar uma GUI para alterar os processos também de forma mais correta.

Podemos tambem criar uma tabela para exibir os servidores disponiveis e poder
pingar nesta tabela de forma que não necessite de uma conexão TCP direto com o servidor
do scheduler e sim com o arquivo sqlite

# ORM

Implementar um esquema mais fácil para lidar com o banco de dados, dado a grande quantidade de migrations/queries do banco...

# Ping server

Criar testes

# Argumentos Incorretos

Tratar a exceção para quando o subprocess falha por conta dos argumentos...

# Processos por servidor

Separar cada processo por servidor para evitar conflitos

# JSON Processos Agendados

Para facilitar na questão do backup, ou migração dos processos agendados para um novo banco de dados...