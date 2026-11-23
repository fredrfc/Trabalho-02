import textwrap


def titulo(texto):
    """Título com barras do mesmo tamanho do texto."""
    barra = '=' * len(texto)
    print(f'\n{barra}\n{texto}\n{barra}')


def _quebrar(linha, maximo, indent=''):
    """Quebra 'linha' em várias linhas que cabem em 'maximo' caracteres,
    sem cortar palavras ao meio quando possível. As linhas de continuação
    recebem 'indent' na frente, para alinhar embaixo do texto original."""
    partes = textwrap.wrap(
        linha, width=maximo,
        subsequent_indent=indent,
        break_long_words=True,
        break_on_hyphens=False,
    )
    return partes or ['']


def caixa(linhas, maximo=80):
    """Mostra as linhas entre barras do tamanho da linha mais longa (limitado ao tamanho do terminal)."""
    linhas_quebradas = []
    for linha in linhas:
        linhas_quebradas.extend(_quebrar(linha, maximo))

    largura = max((len(linha) for linha in linhas_quebradas), default=0)
    print('\n' + '=' * largura)
    for linha in linhas_quebradas:
        print(linha)
    print('=' * largura)


def tabela(cabecalhos, linhas):
    """Tabela com colunas alinhadas e barras do tamanho exato das linhas."""
    linhas = [[str(celula) for celula in linha] for linha in linhas]
    larguras = [
        max([len(cabecalho)] + [len(linha[i]) for linha in linhas])
        for i, cabecalho in enumerate(cabecalhos)
    ]
    formato = ' | '.join(f'{{:<{largura}}}' for largura in larguras)
    cabecalho = formato.format(*cabecalhos)
    print('\n' + '=' * len(cabecalho))
    print(cabecalho)
    print('-' * len(cabecalho))
    for linha in linhas:
        print(formato.format(*linha))
    print('=' * len(cabecalho))


def ficha(titulo_ficha, itens, maximo=80):
    """Ficha com título e campos 'Rótulo : valor' alinhados em coluna.

    itens = lista em que cada item é:
      - uma tupla (rótulo, valor): vira uma linha 'Rótulo : valor' alinhada, ou
      - um texto: é impresso como está.

    Linhas maiores que 'maximo' são quebradas em várias linhas (sem cortar
    nenhuma informação); as linhas de um campo 'Rótulo : valor' continuam
    alinhadas embaixo do valor.
    """
    rotulos = [item[0] for item in itens if isinstance(item, tuple)]
    largura_rotulo = max((len(rotulo) for rotulo in rotulos), default=0)

    linhas = []
    for item in itens:
        if isinstance(item, tuple):
            primeira = f'{item[0]:<{largura_rotulo}} : {item[1]}'
            indent = ' ' * (largura_rotulo + 3)   # alinha sob o início do valor
        else:
            primeira = item
            indent = ''
        linhas.extend(_quebrar(primeira, maximo, indent))

    titulo_quebrado = _quebrar(titulo_ficha, maximo)
    largura = max(len(linha) for linha in titulo_quebrado + linhas)

    print('\n' + '=' * largura)
    for linha in titulo_quebrado:
        print(linha)
    print('-' * largura)
    for linha in linhas:
        print(linha)
    print('=' * largura)
