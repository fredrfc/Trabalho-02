from vulnerabilidade import Vulnerabilidade

class Equipamento:
    tipo = None
    fator_exposicao = 1.0
    
    def __init__(self,id_ativo, hostname, responsavel, setor):
        self.id = id_ativo
        self.hostname = hostname
        self.responsavel = responsavel
        self.setor = setor
        self.vulnerabilidades = []
        self.dependencias = {}

    def para_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'hostname': self.hostname,
            'responsavel': self.responsavel,
            'setor': self.setor,
            'vulnerabilidades': [v.para_dict() for v in self.vulnerabilidades],
            'dependencias': self.dependencias,
        }
    
    def de_dict(cls, d):
        e = cls(d['id'], d['hostname'], d['responsavel'], d['setor'])
        e.vulnerabilidades = [Vulnerabilidade.de_dict(v) for v in d['vulnerabilidades']]
        e.dependencias = d.get('dependencias', {})
        return e
    
class Notebook(Equipamento):
    tipo = 'NOTEBOOK'
    fator_exposicao = 0.8

class Roteador(Equipamento):
    tipo = 'ROTEADOR'
    fator_exposicao = 1.0

class Servidor(Equipamento):
    tipo = 'SERVIDOR'
    fator_exposicao = 1.2

class BancoDeDados(Equipamento):
    tipo = 'BANCO_DE_DADOS'
    fator_exposicao = 1.5

FABRICA = {c.tipo: c for c in (Notebook, Roteador, Servidor, BancoDeDados)}
