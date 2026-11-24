# trab02_2026_2_12621cbs223

Sistema de inventário de ativos de TI e vulnerabilidades, em Python (orientação a objetos),
com cálculo de risco por álgebra linear. A interface é um menu no terminal, e a aplicação
é executada em um container Docker, gerenciado pelo Docker Compose.

## Identificador do projeto

`trab02_2026_2_12621cbs223` é usado como nome do diretório, do repositório, do projeto
compose, do container e da imagem. O Docker exige nomes de imagem em minúsculas, por isso
a matrícula aparece em minúsculas em todos os nomes.

## Estrutura

```
trab02_2026_2_12621cbs223/
├── Dockerfile             # receita da imagem
├── compose.yaml           # como executar o container (nome, volume, terminal)
├── requirements.txt       # dependências Python (numpy)
├── README.md
├── .dockerignore
├── .gitignore
├── data/                  # volume: guarda o arquivo.json entre reinicializações
├── classes.py             # enumerações (tipos, severidade, status)
├── equipamentos.py        # classe Equipamento e subclasses
├── vulnerabilidade.py     # classe Vulnerabilidade
├── inventario.py          # regras de negócio e persistência em JSON
├── risco.py               # modelo de risco (sistema linear)
├── excecoes.py
├── formatacao.py
└── main.py                # menu interativo
```

## Pré-requisitos

- Docker Engine com o plugin Compose. Confira com:

```bash
docker --version
docker compose version
```

- Seu usuário deve poder usar o Docker sem `sudo` (grupo `docker`).

## Construção (build)

1. Obtenha o código e entre na pasta do projeto:

```bash
git clone <https://github.com/fredrfc/Trabalho-02.git> trab02_2026_2_12621cbs223
cd trab02_2026_2_12621cbs223
```

2. Construa a imagem:

```bash
docker compose build
```

Esse comando lê o `Dockerfile`, instala as dependências do `requirements.txt` (numpy) e
copia o código para dentro da imagem `trab02_2026_2_12621cbs223`.

## Execução

1. Inicie o container em segundo plano:

```bash
docker compose up -d
```

2. Confirme que está no ar (coluna `STATUS` com `Up ...`):

```bash
docker ps
```

3. Conecte-se ao menu:

```bash
docker attach --detach-keys="ctrl-x" trab02_2026_2_12621cbs223
```

Pressione `Enter` se a tela estiver em branco. Para **sair sem parar** o programa, use
`Ctrl+X`. Não use `Ctrl+C` nem a opção "Sair" do menu: elas encerram o programa (o
container reinicia sozinho em seguida, e os dados já estão salvos).

Depois de alterar o código, reconstrua e reinicie com:

```bash
docker compose up -d --build
```

## Persistência dos dados (volume)

Os dados ficam em `data/arquivo.json`, no computador (ou servidor) que executa o
`docker compose`. A pasta `data/` é montada em `/data` dentro do container (veja
`volumes:` no `compose.yaml`) e o programa grava nela por meio da variável `DATA_FILE`.
Por isso os dados continuam disponíveis depois de parar, apagar ou recriar o container.

O arquivo é uma lista (array) de objetos JSON, um por equipamento, com suas
vulnerabilidades e dependências.

## Verificar o funcionamento

```bash
docker ps                                        # STATUS: "Up ..." (há quanto tempo está no ar)
docker logs --tail 20 trab02_2026_2_12621cbs223
docker inspect --format '{{.State.Status}} desde {{.State.StartedAt}} | reinicios: {{.RestartCount}}' trab02_2026_2_12621cbs223
```

Para verificar a execução por 24 horas, registre a saída desses comandos no início e depois
de 24 horas.

## Parar e remover

```bash
docker compose down          # remove o container; os dados em data/ permanecem
```

## Portas

Nenhuma porta é mapeada: a aplicação funciona exclusivamente pelo terminal.
