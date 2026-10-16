from enum import Enum

class Severidade(Enum):
    BAIXA = 'Baixa'
    MEDIA = 'Média'
    ALTA = 'Alta'
    CRITICA = 'Crítica'

class Status(Enum):
    ABERTA = 'Aberta'
    EM_MANUTENCAO = 'Em manutenção'
    CORRIGIDA = 'Corrigida'
    ACEITA_COMO_RISCO = 'Aceita como risco'

class TipoAtivo(Enum):
    NOTEBOOK = 1
    ROTEADOR = 2
    SERVIDOR = 3
    BANCO_DE_DADOS = 4
