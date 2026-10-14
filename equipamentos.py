from vulnerabilidade import Vulnerabilidade

class Equipamento:
    tipo = None
    
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
    
    @classmethod
    def de_dict(cls, dados):
        e = cls(dados['id'], dados['hostname'], dados['responsavel'], dados['setor'])
        e.vulnerabilidades = [Vulnerabilidade.de_dict(v) for v in dados['vulnerabilidades']]
        e.dependencias = dados.get('dependencias', {})
        return e
    
class Notebook(Equipamento):
    tipo = 'NOTEBOOK'

class Roteador(Equipamento):
    tipo = 'ROTEADOR'

class Servidor(Equipamento):
    tipo = 'SERVIDOR'

class BancoDeDados(Equipamento):
    tipo = 'BANCO_DE_DADOS'

FABRICA = {c.tipo: c for c in (Notebook, Roteador, Servidor, BancoDeDados)}
