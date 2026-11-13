from classes import Status, TipoAtivo
from excecoes import ValidacaoError
from inventario import Inventario
from risco import calculo_riscos


class Menu:
    def __init__(self, inventario):
        self.inv = inventario
        self.acoes = {
            '1': self.listar_ativos,
            '2': self.buscar_ativo,
            '3': self.cadastrar_ativo,
            '4': self.atualizar_ativo,
            '5': self.remover_ativo,
            '6': self.cadastrar_vulnerabilidade,
            '7': self.listar_vulnerabilidades,
            '8': self.atualizar_vulnerabilidade,
            '9': self.cadastrar_dependencia,
            '10': self.consultar_risco
        }

    def exibir(self):
        print('\n' + '=' * 30)
        print('SISTEMA DE CADASTRO DE ATIVOS')
        print('=' * 30)
        print('1. Listar todos os ativos')
        print('2. Buscar ativo')
        print('3. Cadastrar novo ativo')
        print('4. Atualizar ativo')
        print('5. Remover ativo')
        print('6. Cadastrar vulnerabilidade')
        print('7. Listar vulnerabilidades')
        print('8. Atualizar vulnerabilidade')
        print('9. Cadastrar dependências')
        print('10. Consultar risco')
        print('11. Sair')

    def ler_int(self, texto):
        valor = input(texto).strip()
        if not valor.isdigit():
            raise ValidacaoError('Digite um número inteiro positivo.')
        return int(valor)
    
    def converter_int(self, texto):
        texto = texto.strip()
        if not texto.isdigit():
            raise ValidacaoError('Deve ser um número inteiro positivo.')
        convertido = int(texto)
        return convertido

    def perguntar(self, texto, tratar, tentativas=3):
        for tentativa in range(1, tentativas + 1):
            try:
                return tratar(input(texto))
            except ValidacaoError as e:
                print(f'Erro: {e}')
                if tentativa < tentativas:
                    print(f'\nTente novamente ({tentativa}/{tentativas}).\n')
        raise ValidacaoError('Muitas tentativas inválidas. Operação cancelada.')

    def escolher_status(self):
        lista = list(Status)
        print('\nOPÇÕES DE STATUS:')
        for i, s in enumerate(lista, 1):
            print(f'{i}. {s.name}')

        def validar_escolha_status(texto):
            n = self.converter_int(texto)
            if not 1 <= n <= len(lista):
                raise ValidacaoError('Opção de status inválida.')
            return lista[n - 1].name
        
        return self.perguntar('Digite o número correspondente ao status da vulnerabilidade: ', validar_escolha_status)

    def mostrar_ativo(self, e):
        print('\n' + '=' * 30)
        print(f'ID: {e.id}')
        print(f'Hostname: {e.hostname}')
        print(f'Tipo: {e.tipo}')
        print(f'Responsável: {e.responsavel}')
        print(f'Setor: {e.setor}')
        print(f'Vulnerabilidades: {len(e.vulnerabilidades)}')
        for v in e.vulnerabilidades:
            print(f'  - {v.id}: {v.descricao} [CVSS {v.cvss} | {v.status}]')
        print(f'Dependências: {e.dependencias if e.dependencias else "Nenhuma"}')
        if e.dependencias:
            for origem, fracao in e.dependencias.items():
                print(f'Herda {fracao: .0%} do ativo {origem}')
        print('=' * 30)

    # ATIVOS
    def listar_ativos(self):
        ativos = self.inv.listar_ativos()
        if not ativos:
            print('\nAinda não foi cadastrado nenhum ativo.')
            return
        print(f'\nAtivos cadastrados ({len(ativos)}):')
        print('=' * 72)
        for e in ativos:
            print(f'ID {e.id} | {e.hostname} | {e.tipo} | {e.responsavel} | {e.setor}'
                  f' | {len(e.vulnerabilidades)} vulnerabilidade(s)')
        print('=' * 72)

    def buscar_ativo(self):
        print('\n1. Buscar pelo ID')
        print('2. Buscar pelo hostname')
        escolha = input('Digite 1 ou 2: ').strip()

        if escolha == '1':
            equip = self.perguntar('Digite o ID de um ativo para buscá-lo: ', lambda t: self.inv.buscar_id(self.converter_int(t)))
        elif escolha == '2':
            equip = self.perguntar('Digite o hostname de um ativo para buscá-lo: ', self.inv.buscar_hostname)
        else:
            raise ValidacaoError('Opção de busca inválida.')

        self.mostrar_ativo(equip)

    def escolher_tipo(self):
        tipos = list(TipoAtivo)
        print('\nTIPOS DE ATIVOS:')
        for i, t in enumerate(tipos, 1):
            print(f'{i}. {t.name}')

        def validar(texto):
            n = self.converter_int(texto)
            if not 1 <= n <= len(tipos):
                raise ValidacaoError(f'{n} não é uma opção válida.')
            return tipos[n - 1].name
        
        return self.perguntar('Digite o número correspondente ao tipo do ativo: ', validar)

    def cadastrar_ativo(self):
        id_ativo = self.perguntar('Digite o ID do novo ativo: ', lambda t: self.inv.validar_id_novo(self.converter_int(t)))
        hostname = self.perguntar('Digite o hostname: ', self.inv.validar_hostname)
        responsavel = self.perguntar('Digite o nome do responsável pelo ativo: ', lambda t: self.inv.validar_texto(t, 'responsável'))
        setor = self.perguntar('Digite o setor/localização: ', lambda t: self.inv.validar_texto(t, 'setor'))
        tipo = self.escolher_tipo()
        
        self.inv.cadastrar_ativo(tipo, id_ativo, hostname, responsavel, setor)
        print('\nSucesso! O ativo foi cadastrado.')

    def atualizar_ativo(self):
        id_ativo = self.perguntar('Digite o ID do ativo a ser atualizado: ', lambda t: self.inv.buscar_id(self.converter_int(t)))
        equip = self.inv.buscar_id(id_ativo)
        self.mostrar_ativo(equip)

        print('\nPressione [ENTER] para manter o valor atual.')
        hostname = input(f'Novo hostname [{equip.hostname}]: ')
        responsavel = input(f'Novo responsável [{equip.responsavel}]: ')
        setor = input(f'Novo setor [{equip.setor}]: ')

        self.inv.atualizar(id_ativo, hostname, responsavel, setor)
        print(f'\nSucesso! O ativo {id_ativo} foi atualizado.')

    def remover_ativo(self):
        id_ativo = self.perguntar('Digite o ID do ativo a ser removido: ', lambda t: self.inv.buscar_id(self.converter_int(t)))
        equip = self.inv.buscar_id(id_ativo)
        self.mostrar_ativo(equip)

        confirmacao = input('\nTem certeza que deseja remover este ativo? [s/n]: ').strip().lower()
        if confirmacao == 'n':
            print('Operação cancelada.')
            return
        elif confirmacao == 's':
            self.inv.remover(id_ativo)
            print(f'\nSucesso! O ativo {id_ativo} foi removido do sistema.')
        else:
            raise ValidacaoError('Digite [s] ou [n].')

    # VULNERABILIDADES
    def cadastrar_vulnerabilidade(self):
        equip = self.perguntar('Digite o ID de um ativo cadastrado: ', lambda t: self.inv.buscar_id(self.converter_int(t)))
        
        id_vuln = self.perguntar('Digite o ID da vulnerabilidade (ex: CVE-2026-9855): ', lambda t: self.inv.validar_id_vuln(equip, t))

        descricao = self.perguntar('Escreva a descrição: ', lambda t: self.inv.validar_texto(t, 'descrição'))

        categoria = self.perguntar('Escreva a categoria da vulnerabilidade (ex: Software desatualizado): ', lambda t: self.inv.validar_texto(t, 'categoria'))

        cvss = self.perguntar('Digite o CVSS da vulnerabilidade (0 a 10): ', lambda t: self.inv.validar_cvss_consistente(id_vuln, self.inv.validar_cvss(t)))
        
        status = self.escolher_status()
        
        data = self.perguntar('Digite a data de identificação (DD/MM/AAAA): ', self.inv.validar_data)

        self.inv.cadastrar_vulnerabilidade(equip.id, id_vuln, descricao, categoria, cvss, status, data)
        print('\nSucesso! A vulnerabilidade foi cadastrada.')

    def listar_vulnerabilidades(self):
        pares = self.inv.listar_vulnerabilidades()
        if not pares:
            print('\nNenhuma vulnerabilidade cadastrada.')
            return

        print(f'\nVulnerabilidades cadastradas ({len(pares)})')
        print('=' * 40)
        for equip, v in pares:
            print(f'Ativo: {equip.hostname} (ID: {equip.id})')
            print(f'ID: {v.id}')
            print(f'Descrição: {v.descricao}')
            print(f'Categoria: {v.categoria}')
            print(f'CVSS: {v.cvss}')
            print(f'Status: {v.status}')
            print(f'Data: {v.data}')
            print('=' * 40)

    def atualizar_vulnerabilidade(self):
        id_ativo = self.perguntar('Digite o ID do ativo para atualizar as vulnerabilidades dele: ', lambda t: self.inv.buscar_id(self.converter_int(t)))
        equip = self.inv.buscar_id(id_ativo)

        if not equip.vulnerabilidades:
            raise ValidacaoError('Esse ativo não possui vulnerabilidades cadastradas.')

        print(f'\nVulnerabilidades do ativo {equip.hostname}:')
        for v in equip.vulnerabilidades:
            print(f'- {v.id}: {v.descricao} [{v.status}]')

        id_vuln = input('\nDigite o ID da vulnerabilidade a ser atualizada: ')

        print('\nPressione [ENTER] para manter o valor atual.')
        descricao = input('Nova descrição: ')
        categoria = input('Nova categoria: ')

        status = None
        if input('Deseja alterar o status? [s/n]: ').strip().lower() == 's':
            status = self.escolher_status()

        self.inv.atualizar_vulnerabilidade(id_ativo, id_vuln, descricao, categoria, status)
        print('\nSucesso! A vulnerabilidade foi atualizada.')

    def cadastrar_dependencia(self):
        id_ativo = self.perguntar('Digite o ID do ativo que HERDA o risco: ', lambda t: self.inv.buscar_id(self.converter_int(t)))
        id_dependencia = self.ler_int('Digite o ID do ativo DE QUEM ele herda o risco: ')
        fracao = input('Digite a fração herdada (ex: 0.5; deve ser maior ou igual a 0 e menor do que 1): ').replace(',', '.')

        self.inv.cadastrar_dependencia(id_dependencia, id_ativo, fracao)

        print('\nSucesso! A dependência foi adicionada ao sistema.')

    def consultar_risco(self):
        resultados = calculo_riscos(self.inv)

        if not resultados:
            print('\nNão há nenhum ativo para ser consultado.')
            return

        print('=' * 63)
        for r in resultados:
            print(f'ID: {r["id"]} | Hostname: {r["hostname"]} | Risco Próprio: {r["risco_proprio"]:.2f} | Risco Efetivo: {r["risco_efetivo"]:.2f}')
        print('=' * 63)

    # LAÇO PRINCIPAL
    def executar(self):
        while True:
            self.exibir()
            opcao = input('\nDigite o número da opção: ').strip()

            if opcao == '11':
                print('\nEncerrando o programa...')
                break

            acao = self.acoes.get(opcao)
            if acao is None:
                print('\nOpção inválida (escolha de 1 a 11).')
                continue

            try:
                acao()
            except (ValidacaoError, ValueError) as e:
                print(f'\nErro: {e}')


if __name__ == '__main__':
    try:
        Menu(Inventario()).executar()
    except (KeyboardInterrupt, EOFError):
        print('\nPrograma encerrado pelo usuário.')
