# send_project
> Esqueleto para disparo de envio.
> Montado em hexagonal 
> Banco de dados MYSQL 
## Padrao de logs

1. Níveis de Log (Quando usar cada um)

DEBUG: Detalhes técnicos (ex: "Convertendo model para entity"). Útil apenas para o desenvolvedor.

INFO: Eventos significativos do negócio (ex: "Usuário X cadastrado com sucesso").

WARNING: Algo estranho aconteceu, mas o sistema não parou (ex: "Tentativa de cadastro de CPF já existente").

ERROR: Algo quebrou uma operação (ex: "Erro ao conectar no banco"). É aqui que você captura as Exceptions.

CRITICAL: O sistema inteiro vai cair (ex: "Disco cheio" ou "Sem memória").

## Banco de dados

## Mappers

## Repositorios

### PersonRepositorio 

#### Cread
> Criação de usuarios