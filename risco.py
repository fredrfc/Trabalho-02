import numpy as np

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
        for v in ativo.vulnerabilidades:
            coluna = posicao_vulnerabilidade[id_vuln]
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

    return posicao_ativo, M, v

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
