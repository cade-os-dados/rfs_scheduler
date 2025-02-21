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

Criar testes e a GUI

# Argumentos Incorretos

Tratar a exceção para quando o subprocess falha por conta dos argumentos...

# Processos Instantâneos

Precisamos adaptar o scheduler para quando rodamos um processo instantâneo, ele priorizar o processo instantâneo em detrimento do agendado. Neste caso talvez precisaremos utilizar eventos para comunicação entre as threads e talvez devemos adaptar o status do Scheduler Core para suportar running, waiting e stoped, algo do tipo, não só running True ou False. E com base no status modular o seu comportamento...