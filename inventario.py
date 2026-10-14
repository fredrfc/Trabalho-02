from excecoes import ValidacaoError
from equipamentos import FABRICA

class Inventario:
    def __init__(self):
        self.equipamentos = {}

    def cadastrar(self, tipo, id_ativo, hostname, responsavel, setor):
        if tipo not in FABRICA:
            raise ValidacaoError(f'Tipo inválido: {tipo}')

        if not hostname.strip() or not responsavel.strip() or not setor.strip():
            raise ValidacaoError('Nenhum campo pode estar vazio.')

        if id_ativo in self.equipamentos:
            raise ValidacaoError(f'Já existe um ativo com o ID: {id_ativo}')

        for equip in self.equipamentos.values():
            if equip.hostname.lower() == hostname.lower():
                raise ValidacaoError('Já existe um ativo com esse hostname.')

        equip = FABRICA[tipo](id_ativo, hostname.strip(), responsavel.strip(), setor.strip())
        
        self.equipamentos[id_ativo] = equip
        
        return equip

    def buscar_id(self, id_ativo):
        if id_ativo not in self.equipamentos:
            raise ValidacaoError('Não existe um ativo cadastrado com esse ID.')
        return self.equipamentos[id_ativo]

    def buscar_hostname(self, hostname):
        alvo = hostname.strip().lower()
        for equip in self.equipamentos.values():
            if equip.hostname.lower() == alvo:
                return equip
        raise ValidacaoError('Não existe um ativo cadastrado com esse hostname.')
      
