import pprint
from enum import Enum

class TipoAtivo(Enum):
    NOTEBOOK = 1
    ROTEADOR = 2
    SERVIDOR = 3
    BANCO_DE_DADOS = 4

class Equipamento:
    def __init__(self, id_ativo, hostname, responsavel, setor):
        self.id = id_ativo
        self.host = hostname
        self.resp = responsavel
        self.setor = setor
        self.vulns = []

    # Permite converter o objeto de volta para dicionário se precisar salvar em JSON
    def para_dicionario(self):
        return {
            'hostname': self.host,
            'responsavel': self.resp,
            'setor': self.setor,
            'tipo': self.__class__.__name__, # Pega automaticamente o nome da classe
            'vulnerabilidades': self.vulns
        }

# Subclasses herdam o comportamento, mas representam tipos reais
class Notebook(Equipamento):
    pass

class Roteador(Equipamento):
    pass

class Servidor(Equipamento):
    pass

class BancoDeDados(Equipamento):
    pass

class GerenciadorAtivos:
    def __init__(self):
        # Em vez de um dicionário global solto, ele pertence ao Gerenciador
        self.dict_ativos = {} 

    def cadastrar_ativo(self):
        try:
            print('=' * 30)
            print('SISTEMA DE CADASTRO DE ATIVOS')
            print('=' * 30)
            
            # Validação do ID
            id_input = input('Qual é o ID do novo ativo?: ').strip()
            if not id_input.isdigit():
                print('\nErro! O ID deve ser um número inteiro positivo!')
                return False
            
            id_ativo = int(id_input)

            if id_ativo in self.dict_ativos:
                print('\nJá existe um ativo cadastrado com esse ID.')
                # Exibe os dados do objeto existente convertidos em dicionário
                pprint.pprint(self.dict_ativos[id_ativo].para_dicionario())
                return False
    
            # Validação do Hostname
            hostname = input('\nQual é o nome/hostname do ativo?: ').strip()
            if hostname == '':
                print('\nO campo para hostname não pode estar vazio!')
                return False
    
            for ativo in self.dict_ativos.values():
                if ativo.host.lower() == hostname.lower():
                    print('\nJá existe um ativo cadastrado com esse nome/hostname!')
                    return False
            
            # Validação do responsável e do setor
            resp = input('Quem é o responsável técnico pelo ativo?: ').strip()
            setor = input('Qual é a localização/setor do ativo?: ').strip()
            if not resp or not setor:
                print('\nCampos obrigatórios vazios!')
                return False
    
            # Menu do Enum
            print('\nOPÇÕES VÁLIDAS PARA TIPO DE ATIVO:')
            for i, tipo_enum in enumerate(TipoAtivo, 1):
                print(f'{i}. {tipo_enum.name}')
    
            tipo_opcao = input('\nDigite o número correspondente ao tipo do seu ativo: ').strip()
            if tipo_opcao not in [str(i) for i in range(1, len(TipoAtivo) + 1)]:
                print('\nOpção inválida!')
                return False
            
            tipo_escolhido = list(TipoAtivo)[int(tipo_opcao) - 1]

            # POLIMORFISMO
            if tipo_escolhido == TipoAtivo.NOTEBOOK:
                novo_ativo = Notebook(id_ativo, hostname, resp, setor)
            elif tipo_escolhido == TipoAtivo.ROTEADOR:
                novo_ativo = Roteador(id_ativo, hostname, resp, setor)
            elif tipo_escolhido == TipoAtivo.SERVIDOR:
                novo_ativo = Servidor(id_ativo, hostname, resp, setor)
            elif tipo_escolhido == TipoAtivo.BANCO_DE_DADOS:
                novo_ativo = BancoDeDados(id_ativo, hostname, resp, setor)

            self.dict_ativos[id_ativo] = novo_ativo
            
            # Aqui você chamaria a sua função de persistência externa passando os dados estruturados
            # salvar_info(self.exportar_para_salvamento()) 
            
            print('\nSucesso! O seu ativo foi cadastrado no sistema!')
            return True
    
        except Exception as e:
            print(f'\nErro inesperado: {e}')
            return False

    def exportar_para_salvamento(self):
        return {id_at: obj.para_dicionario() for id_at, obj in self.dict_ativos.items()}
