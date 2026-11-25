# trab02_2026_2_12621cbs223

Sistema de inventário de ativos de TI e vulnerabilidades, em Python (orientação a objetos),
com cálculo de risco por álgebra linear. A interface é um menu no terminal, e a aplicação
é executada em um container Docker, gerenciado pelo Docker Compose.

## Funcionalidades

- Cadastro e consulta de ativos de TI e de suas vulnerabilidades.
- Representação dos equipamentos por classes e subclasses em Python.
- Associação de dependências entre equipamentos.
- Cálculo do risco próprio e do risco efetivo com NumPy.
- Validação do sistema linear e da solução numérica.
- Persistência em JSON e inicialização com dados de exemplo.
- Interface interativa no terminal e execução em Docker.

## Identificador do projeto

`trab02_2026_2_12621cbs223` é utilizado como nome do diretório local, do projeto Docker Compose, do container e da imagem. A matrícula é representada em letras minúsculas para atender às regras de nomenclatura das imagens Docker. O repositório no GitHub chama-se `Trabalho-02`.

## Estrutura

```
trab02_2026_2_12621cbs223/
├── Dockerfile             # receita da imagem
├── compose.yaml           # como executar o container (nome, volume, terminal)
├── requirements.txt       # dependências Python (numpy)
├── README.md
├── .dockerignore
├── .gitignore
├── data/                  # diretório persistente (bind mount)
├── dados_exemplo.json     # dados de exemplo para a aplicação
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

- Git, para obter o código-fonte.
- Acesso autorizado ao Docker, conforme as regras do ambiente de execução.
- Permissão de leitura e escrita no diretório `data/` para o usuário do container.

O `compose.yaml` define `user: 1040:1041` (UID e GID). Em Linux, esses identificadores devem ser compatíveis com as permissões do diretório `data/` no host. Em outro ambiente, pode ser necessário adequar essa configuração. No servidor compartilhado, siga as orientações administrativas e não utilize permissões indiscriminadas como `chmod 777`.

## Construção (build)

1. Obtenha o código e entre na pasta do projeto:

```bash
git clone https://github.com/fredrfc/Trabalho-02.git trab02_2026_2_12621cbs223
cd trab02_2026_2_12621cbs223
```

2. Construa a imagem:

```bash
docker compose build
```

Esse comando lê o `Dockerfile`, instala as dependências do `requirements.txt` (numpy) e
copia o código e o `dados_exemplo.json` para dentro da imagem `trab02_2026_2_12621cbs223`. A imagem utiliza Python 3.12.

## Execução

1. Inicie o container em segundo plano:

```bash
docker compose up -d
```

2. Confirme que está no ar (coluna `STATUS` com `Up ...`):

```bash
docker compose ps
```

3. Conecte-se ao menu:

```bash
docker attach --detach-keys="ctrl-x" trab02_2026_2_12621cbs223
```

Pressione `Enter` se a tela estiver em branco. Para **desconectar sem parar** o programa, use `Ctrl+X`, conforme definido no comando acima.

Evite `Ctrl+C` e a opção "Sair" do menu durante o período de funcionamento contínuo: essas ações podem encerrar o processo principal e provocar a reinicialização do container. A política `restart: unless-stopped` não substitui a verificação do estado da aplicação.

Depois de alterar o código, reconstrua e reinicie com:

```bash
docker compose up -d --build
```

Esse procedimento pode recriar o container e interromper a contagem de funcionamento contínuo. Alterações apenas no README não exigem reconstrução da imagem.

## Persistência dos dados (volume)

Os dados ficam em `data/arquivo.json`, no computador (ou servidor) que executa o
`docker compose`. A pasta `data/` é montada em `/data` dentro do container (veja
`volumes:` no `compose.yaml`) e o programa grava nela por meio da variável `DATA_FILE`.
Por isso os dados continuam disponíveis depois de parar, apagar ou recriar o container.

O arquivo é uma lista (array) de objetos JSON, um por equipamento, com suas
vulnerabilidades e dependências.

## Dados de exemplo

O arquivo `dados_exemplo.json` contém quatro ativos (notebook, servidor, roteador e banco de dados), suas vulnerabilidades e dependências. Durante o build, ele é incorporado à imagem em `/app/dados_exemplo.json`.

Na inicialização, o comando definido no Dockerfile verifica se `/data/arquivo.json` existe:

- Se não existir, tenta copiar os dados de exemplo para esse caminho.
- Se existir, preserva o arquivo de persistência, mesmo que esteja vazio.

Assim, o usuário pode testar a aplicação sem cadastrar todos os equipamentos manualmente. Os novos cadastros são armazenados no arquivo de persistência, sem alterar a base de exemplo incorporada à imagem.

Para conferir os dados efetivamente disponíveis no container em execução:

```bash
docker compose exec app cat /data/arquivo.json
```

Caso os dados não apareçam, confira os logs, a existência do arquivo e as permissões do diretório `data/`. Não sobrescreva dados existentes sem realizar um backup.

## Modelo de análise de risco

O módulo `risco.py` utiliza NumPy para calcular o risco dos equipamentos por meio de álgebra linear.

| Símbolo | Significado |
| --- | --- |
| $M$ | Matriz binária de incidência entre equipamentos e vulnerabilidades |
| $v$ | Vetor das severidades CVSS |
| $b$ | Vetor de risco próprio |
| $A$ | Matriz de dependências entre equipamentos |
| $I$ | Matriz identidade |
| $x$ | Vetor de risco efetivo |

### Risco próprio

O risco próprio é calculado pelo produto matricial:

$$
b = Mv
$$

Na implementação atual, apenas vulnerabilidades com status `ABERTA` ou `EM_MANUTENCAO` são consideradas na matriz de incidência. Vulnerabilidades com o mesmo identificador devem apresentar a mesma nota CVSS em todos os ativos.

O modelo permite ponderar o risco próprio pelo fator de exposição de cada equipamento, conforme o seu tipo. A função `calculo_riscos()` utiliza essa ponderação por padrão:

$$
b_i = f_i (Mv)_i
$$

### Risco efetivo

O elemento $A_{ij}$ representa a fração do risco do equipamento $j$ transmitida ao equipamento $i$. O risco efetivo inclui o risco próprio e o risco herdado direta ou indiretamente das dependências:

$$
x = b + Ax
$$

Reorganizando a equação:

$$
(I-A)x = b
$$

A aplicação resolve esse sistema diretamente com `numpy.linalg.solve()`, sem calcular explicitamente a matriz inversa.

### Validações matemáticas

Antes de apresentar os resultados, o módulo verifica:

- As dimensões da matriz de dependências e se os valores numéricos são finitos.
- Se cada fração de dependência pertence ao intervalo $[0,1)$.
- Se a diagonal da matriz é nula (sem autodependências).
- Se a soma dos elementos de cada linha é menor que 1, com tolerância numérica.
- A invertibilidade de $I-A$, por meio do posto da matriz (`numpy.linalg.matrix_rank()`).
- O número de condição do sistema (`numpy.linalg.cond()`), rejeitando valores superiores a $10^8$.
- A consistência da solução, verificando se $(I-A)x$ é aproximadamente igual a $b$ com `numpy.allclose()`.

O módulo retorna o risco próprio e o risco efetivo de cada equipamento, mantendo a precisão de ponto flutuante nos cálculos.

## Verificar o funcionamento

```bash
docker compose ps
docker compose logs --tail=30 app
docker inspect --format '{{.State.Status}} desde {{.State.StartedAt}} | reinicios: {{.RestartCount}}' trab02_2026_2_12621cbs223
```

Para verificar a execução por 24 horas, registre a saída desses comandos no início e depois
de 24 horas. Confira se o container permanece em execução, se o horário de início não mudou e se não houve reinicializações. Esses comandos são consultas e não interrompem a aplicação.

## Parar e remover

```bash
docker compose down          # remove o container; os dados em data/ permanecem
```

O comando deve ser executado na pasta do projeto correto. Não o utilize durante o período obrigatório de funcionamento contínuo. Os arquivos gravados no diretório `data/` permanecem no host.

## Portas

Nenhuma porta é mapeada: a aplicação funciona exclusivamente pelo terminal.
