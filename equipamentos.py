class Equipamento:
    def __init__(self,id_ativo, hostname, responsavel, setor):
        self.id = id_ativo
        self.host = hostname
        self.resp = responsavel
        self.setor = setor
        self.vulns = []

    def para_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "hostname": self.host,
            "responsavel": self.resp,
            "setor": self.setor,
            "vulnerabilidades": [v.para_dict() for v in self.vulns],
            "dependencias": self.dependencias,
        }
    
    def de_dict(cls, d):
        e = cls(d["id"], d["hostname"], d["responsavel"], d["setor"])
        e.vulnerabilidades = [Vulnerabilidade.de_dict(v) for v in d["vulnerabilidades"]]
        e.dependencias = d.get("dependencias", {})
        return e
    
class Notebook(Equipamento):
    def __init__(self, id_ativo, hostname, responsavel, setor):
        super().__init__(id_ativo, hostname, responsavel, setor)
        super().para_dict()
        super().de_dict()

class Roteador(Equipamento):
    def __init__(self, id_ativo, hostname, responsavel, setor):
        super().__init__(id_ativo, hostname, responsavel, setor)
        super().para_dict()
        super().de_dict()

class Servidor(Equipamento):
    def __init__(self, id_ativo, hostname, responsavel, setor):
        super().__init__(id_ativo, hostname, responsavel, setor)
        super().para_dict()
        super().de_dict()

class BancoDeDados(Equipamento):
    def __init__(self, id_ativo, hostname, responsavel, setor):
        super().__init__(id_ativo, hostname, responsavel, setor)
        super().para_dict()
        super().de_dict()