# Serviço Agregador de Dados de APIs Públicas
## Visão Geral
Esta aplicação é um serviço distribuído que, a partir de uma consulta do usuário, agrega dados de duas APIs públicas (OMDB e TMDB) e retorna uma resposta formatada em JSON. O usuário informa o título e o ano do filme, e o sistema retorna um JSON contendo:
- titulo: Título do filme.
- ano: Ano do filme.
- sinopse: Sinopse completa do filme (obtida do OMDB).
- reviews: Uma lista (de até 3 elementos) com as reviews do filme (obtidas do TMDB).
---
## Requisitos
Antes de rodar o código, é necessário:
- Ter o Python 3 instalado.
- Ter uma chave de API válida para OMDB e TMDB.
- Ter a biblioteca requests instalada. Caso não tenha, instale com:
```
pip install requests
```
## Como Executar
- Baixe ou clone o repositório
```
git clone github.com/VRitzel/sistemasdistribuidos_atividade1.git
```
- Substitua as chaves de API no código pelos seus próprios valores:
```
omdb_apikey = "SUA_CHAVE_OMDB"
headers = {
    "Authorization": "Bearer SUA_CHAVE_TMDB"
}
```
- Execute o script
- Insira o título do filme e o ano quando solicitado

## Estrutura do Código
- get_tmdb_id(imdb_id): Obtém o ID do filme no TMDB com base no IMDb ID.
- get_tmdb_reviews(tmdb_id): Obtém até 3 reviews do TMDB.
- get_plot(imdb_id, apikey): Obtém a sinopse do OMDB.

## Execução principal:
- Solicita entrada do usuário.
- Faz chamadas concorrentes para obter dados.
- Agrega os resultados e exibe o JSON final.

