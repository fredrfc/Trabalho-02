class Vulnerabilidade:
    def __init__(self, id_vulnerabilidade, descricao, categoria, cvss, status, data):
        self.id = id_vulnerabilidade
        self.descricao = descricao
        self.categoria = categoria
        self.cvss = cvss
        self.status = status
        self.data = data

    def para_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'cvss': self.cvss,
            'status': self.status,
            'data': self.data,
        }

    @classmethod
    def de_dict(cls, dados):
        return cls(dados["id"], dados["descricao"], dados["categoria"],
               dados["cvss"], dados["status"], dados["data"])
