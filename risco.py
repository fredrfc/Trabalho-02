import numpy as np

STATUS_COM_RISCO = ('ABERTA', 'EM_MANUTENCAO')

def montar_M_v(inventario):
    ativos = inventario.listar_ativos()
    
    posicao_ativo = {}
    for i, ativo in enumerate(ativos):
        posicao_ativo[ativo.id] = i

    ids_vuln = set()
    for ativo in ativos:
        for v in ativo.vulnerabilidades:
            ids_vuln.add(v.id.lower())
    
    posicao_vulnerabilidade = {}
    for j, id_vuln in enumerate(sorted(ids_vuln)):
        posicao_vulnerabilidade[id_vuln] = j

    n = len(ativos)
    m = len(posicao_vulnerabilidade)
    M = np.zeros((n, m))

    for ativo in ativos:
        linha = posicao_ativo[ativo.id]
        for vuln in ativo.vulnerabilidades:
            coluna = posicao_vulnerabilidade[vuln.id.lower()]
            M[linha, coluna] = 1

    v = np.zeros(m)
    visto = {}

    for ativo in ativos:
        for vuln in ativo.vulnerabilidades:
            chave = vuln.id.lower()
            if chave in visto and visto[chave] != vuln.cvss:
                raise ValueError(f'A vulnerabilidade {vuln.id} tem notas CVSS diferentes em ativos distintos.')
            visto[chave] = vuln.cvss
            v[posicao_vulnerabilidade[chave]] = vuln.cvss

    return M, v, posicao_ativo

def calcular_b(inventario, com_fator=False):
    M, v, posicao_ativo = montar_M_v(inventario)
    ativos = inventario.listar_ativos()
    b = M @ v
    if com_fator:
        fatores = []
        for ativo in ativos:
            fatores.append(ativo.fator_exposicao)
        f = np.array(fatores)
        b = f * b
    return b

def montar_A(inventario):
    ativos = inventario.listar_ativos()

    posicao_ativo = {}
    for i, ativo in enumerate(ativos):
        posicao_ativo[ativo.id] = i

    n = len(ativos)
    A = np.zeros((n, n))

    for ativo in ativos:
        i = posicao_ativo[ativo.id]
        for chave, fracao in ativo.dependencias.items():
            origem = int(chave)
            if origem not in posicao_ativo:
                raise ValueError(f'O ativo {ativo.id} depende do ativo {origem}, que não existe.')
            j = posicao_ativo[origem]
            A[i, j] = fracao
    return A

def resolver_risco(b, A):
    b = np.array(b, dtype=float)
    A = np.array(A, dtype=float)
    n = len(b)

    if n == 0:
        return []
    
    if A.shape != (n, n):
        raise ValueError('A deve ser uma matriz quadrada de ordem n.')
    
    if not np.isfinite(A).all() or not np.isfinite(b).all():
        raise ValueError('Os valores devem ser números finitos.')
    
    if (A < 0).any() or (A >= 1).any():
        raise ValueError('As células da matriz A não podem ser menor do que 0 ou maior ou igual a 1.')
    
    if (np.diag(A) != 0).any():
        raise ValueError('Um ativo não pode depender dele mesmo (a diagonal de A deve ser zero).')
    
    if (A.sum(axis=1) >= 1 - 1e-9).any():
        raise ValueError('A soma dos valores de cada linha de A deve ser menor do que 1.')
    
    B = np.eye(n) - A

    if np.linalg.matrix_rank(B) < n:
        raise ValueError('O sistema é singular.')
    
    condicao = np.linalg.cond(B)
    if condicao > 1e8:
        raise ValueError(f'Sistema muito sensível a pequenos erros (cond = {condicao:.2e}); resultado pouco confiável.')
    
    x = np.linalg.solve(B, b)

    if not np.allclose(B @ x, b, rtol=1e-8, atol=1e-10):
        raise ValueError('A solução não passou na conferência.')
    
    return x.tolist()

def calculo_riscos(inventario):
    ativos = inventario.listar_ativos()

    b = calcular_b(inventario)
    A = montar_A(inventario)
    x = resolver_risco(b, A)

    resultado = []
    for i, ativo in enumerate(ativos):
        resultado.append({
            'id': ativo.id,
            'hostname': ativo.hostname,
            'risco_proprio': float(b[i]),
            'risco_efetivo': float(x[i]),
        })
    return resultado
