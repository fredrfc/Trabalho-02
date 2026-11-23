def titulo(texto):
    """Título com barras do mesmo tamanho do texto."""
    barra = '=' * len(texto)
    print(f'\n{barra}\n{texto}\n{barra}')


def caixa(linhas, maximo=80):
    """Mostra as linhas entre barras do tamanho da linha mais longa (limitado ao tamanho do terminal)."""
    largura = min(max((len(linha) for linha in linhas), default=0), maximo)
    print('\n' + '=' * largura)
    for linha in linhas:
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
    """
    rotulos = [item[0] for item in itens if isinstance(item, tuple)]
    largura_rotulo = max((len(rotulo) for rotulo in rotulos), default=0)
    linhas = [
        f'{item[0]:<{largura_rotulo}} : {item[1]}' if isinstance(item, tuple) else item
        for item in itens
    ]
    largura = min(max(len(linha) for linha in [titulo_ficha] + linhas), maximo)
    print('\n' + '=' * largura)
    print(titulo_ficha)
    print('-' * largura)
    for linha in linhas:
        print(linha)
    print('=' * largura)
