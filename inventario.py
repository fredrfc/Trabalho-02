import json
import os
from datetime import datetime
from classes import Status
from equipamentos import FABRICA
from excecoes import ValidacaoError
from vulnerabilidade import Vulnerabilidade


class Inventario:
    def __init__(self, arquivo='arquivo.json'):
        self.arquivo = arquivo
        self.equipamentos = {}
        self.carregar()

    # PERSISTÊNCIA
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

    # ATIVOS
    def cadastrar_ativo(self, tipo, id_ativo, hostname, responsavel, setor):
        if tipo not in FABRICA:
            raise ValidacaoError(f'Tipo inválido: {tipo}')

        if not hostname.strip() or not responsavel.strip() or not setor.strip():
            raise ValidacaoError('Os campos para hostname, responsável e setor devem ser preenchidos.')

        if id_ativo in self.equipamentos:
            raise ValidacaoError(f'Já existe um ativo com o ID: {id_ativo}.')

        for equip in self.equipamentos.values():
            if equip.hostname.lower() == hostname.strip().lower():
                raise ValidacaoError('Já existe um ativo cadastrado com esse hostname.')

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
            if equip.hostname.lower() ==  hostname.strip().lower():
                return equip
        raise ValidacaoError('Não existe um ativo cadastrado com esse hostname.')

    def listar_ativos(self):
        return sorted(self.equipamentos.values(), key=lambda e: e.id)

    def atualizar(self, id_ativo, hostname=None, responsavel=None, setor=None):
        equip = self.buscar_id(id_ativo)

        if hostname is not None and hostname.strip():
            novo = hostname.strip()
            for outro in self.equipamentos.values():
                if outro.id != id_ativo and outro.hostname.lower() == novo.lower():
                    raise ValidacaoError('Já existe um ativo com esse hostname.')
            equip.hostname = novo

        if responsavel is not None and responsavel.strip():
            equip.responsavel = responsavel.strip()

        if setor is not None and setor.strip():
            equip.setor = setor.strip()

        self.salvar()
        return equip

    def remover(self, id_ativo):
        equip = self.buscar_id(id_ativo)
        del self.equipamentos[id_ativo]

        for outro in self.equipamentos.values():
            outro.dependencias.pop(str(id_ativo), None)

        self.salvar()
        return equip

    # VULNERABILIDADES
    def cadastrar_vulnerabilidade(self, id_ativo, id_vuln, descricao, categoria, cvss, status, data):
        equip = self.buscar_id(id_ativo)

        if not id_vuln.strip() or not descricao.strip() or not categoria.strip():
            raise ValidacaoError('Os campos de ID, descrição e categoria devem ser preenchidos.')

        if any(v.id.lower() == id_vuln.strip().lower() for v in equip.vulnerabilidades):
            raise ValidacaoError('Esse ativo já possui uma vulnerabilidade com esse ID.')

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
        except ValueError:
            raise ValidacaoError('Data inválida. Considere o formato DD/MM/AAAA.')

        vuln = Vulnerabilidade(id_vuln.strip(), descricao.strip(), categoria.strip(), cvss, status, data)
        equip.vulnerabilidades.append(vuln)
        self.salvar()
        return vuln

    def listar_vulnerabilidades(self):
        return [(e, v) for e in self.equipamentos.values() for v in e.vulnerabilidades]

    def atualizar_vulnerabilidade(self, id_ativo, id_vuln, descricao=None, categoria=None, status=None):
        equip = self.buscar_id(id_ativo)

        alvo = id_vuln.strip().lower()
        vuln = None
        for v in equip.vulnerabilidades:
            if v.id.lower() == alvo:
                vuln = v
                break
        if vuln is None:
            raise ValidacaoError('Esse ativo não possui uma vulnerabilidade com esse ID.')

        if status is not None and status not in Status.__members__:
            raise ValidacaoError(f'Status inválido: {status}')

        if descricao is not None and descricao.strip():
            vuln.descricao = descricao.strip()
        if categoria is not None and categoria.strip():
            vuln.categoria = categoria.strip()
        if status is not None:
            vuln.status = status

        self.salvar()
        return vuln
        
    def cadastrar_dependencia(self, id_dependencia, id_ativo, fracao):
        equip = self.buscar_id(id_ativo)
        self.buscar_id(id_dependencia)

        if id_dependencia == id_ativo:
            raise ValidacaoError('Um ativo não pode depender dele mesmo.')
    
        try:
            fracao = float(fracao)
        except (TypeError, ValueError):
            raise ValidacaoError('A fração deve ser um número.')
    
        if not 0 <= fracao < 1:
            raise ValidacaoError('A fração deve ser maior ou igual a 0 e menor do que 1.')  
    
        soma = 0
        for chave, valor in equip.dependencias.items():
            if chave != str(id_dependencia):
                soma += valor
        if soma + fracao >= 1:
            raise ValidacaoError('A soma das frações de um ativo deve ser menor do que 1.')
    
        equip.dependencias[str(id_dependencia)] = fracao
        self.salvar()
        return equip
