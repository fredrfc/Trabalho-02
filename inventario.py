from datetime import datetime
from classes import Status
from vulnerabilidade import Vulnerabilidade
from excecoes import ValidacaoError
from equipamentos import FABRICA
import json
import os

class Inventario:
    def __init__(self, arquivo='arquivo.json'):
        self.arquivo = arquivo
        self.equipamentos = {}
        self.carregar()

    def salvar(self):
        dados = [e.para_dict() for e in self.equipamentos.values()]
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar(self):
        if not os.path.exists(self.arquivo):
            return
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.equipamentos = {}
            for d in dados:
                equip = FABRICA[d['tipo']].de_dict(d)
                self.equipamentos[equip.id] = equip

    def cadastrar_ativo(self, tipo, id_ativo, hostname, responsavel, setor):
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
        self.salvar() 
        return equip

    def buscar_id(self, id_ativo):
        if id_ativo not in self.equipamentos:
            raise ValidacaoError('Não existe um ativo cadastrado com esse ID.')
        return self.equipamentos[id_ativo]

    def buscar_hostname(self, hostname):
        for equip in self.equipamentos.values():
            if equip.hostname.strip().lower() == hostname.lower():
                return equip
        raise ValidacaoError('Não existe um ativo cadastrado com esse hostname.')
        
    def cadastrar_vulnerabilidade(self, id_ativo, id_vuln, descricao, categoria, cvss, data, status):
        equip = self.buscar_id(id_ativo)

        if not id_vuln.strip() or not descricao.strip() or not categoria.strip():
            raise ValidacaoError('Os campos de ID, descrição e categoria devem ser preenchidos.')
            
        try:
            cvss = float(cvss)
        except (TypeError, ValueError):
            raise ValidacaoError('O CVSS deve ser um número.')
            
        if not 0 <= cvss <= 10:
            raise ValidacaoError('O CVSS deve ser um número entre 0 e 10.')
            
        if status not in Status.__members__:
            raise ValidacaoError(f'Status inválido: {status}')
            
        try:
            datetime.strptime(data, '%d/%m/%Y')
        except (ValueError):
            raise ValidacaoError('Data inválida. Considere o formato DD/MM/AAAA.')
            
        vuln = Vulnerabilidade(id_vuln.strip(), descricao.strip(), categoria.strip(), cvss, data, status)
        equip.vulnerabilidades.append(vuln)
        self.salvar()
        return vuln
        
    def listar_vulnerabilidades(self):
        lista = []
        for equip in self.equipamentos.values():
            for vuln in equip.vulnerabilidades:
                lista.append((equip, vuln))
        return lista
