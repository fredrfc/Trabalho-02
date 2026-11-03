import numpy as np
from inventario import Inventario

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
            if chave in visto and 


    return posicao_ativo, posicao_vulnerabilidade, M


