from dependencias.clientesCRUD import *
from dependencias.servicoCRUD import *
from dependencias.relatorio import *

#TRABALHO: LARA RECK, PEDRO BORSATO, PEDRO LUCAS

def main():
    while True:
        print('-*'*15)
        escolha = int(input('voce quer editar um cliente, uma ordem de servico ou fazer um relatorio? \n(1 para cliente, 2 para ordem de servico, 3 para relatorio, 4 para sair) \n '))
        
        if escolha == 1:
            subEscolha = int(input("""1 para cadastrar novo cliente
2 para ver as informacoes do cliente
3 para editar alguma informação do cliente
4 para deletar algum cliente \n """))
            cpf = str(input('qual o cpf do cliente? '))
            match subEscolha:
                case 1:
                    nome = str(input('qual o nome do cliente? '))
                    telefone = str(input('qual o telefone do cliente? '))
                    email = str(input('qual o email do cliente? '))
                    createCliente(cpf, nome, telefone, email)

                case 2:
                    readCliente(cpf)

                case 3:
                    updateClientes(cpf)

                case 4:
                    deleteCliente(cpf)
                case _:
                    print('escolha um CPF valido!')
                    continue

        elif escolha == 2:
            subEscolha = int(input("""1 para cadastrar nova ordem de servico
2 para ver as informacoes da ordem de servico
3 para editar alguma informação da ordem de servico
4 para deletar alguma ordem de servico\n """))
            match subEscolha:
                case 1:
                    cpf = str(input('qual o cpf do cliente? '))
                    valor = float(input('qual o valor da ordem? '))
                    status = str('qual o status da ordem? ')
                    createServico(cpf, valor, status)

                case 2:
                    id = int(input('qual o ID da ordem? '))
                    readServico(id)

                case 3:
                    id = int(input('qual o ID da ordem? '))
                    updateServico(id)

                case 4:
                    id = int(input('qual o ID da ordem? '))
                    deleteServico(id)
                case _:
                    print('escolha uma opcao valida!')
                    continue
        
        elif escolha == 3:
            gerarRelatorio()

        elif escolha == 4:
            print('por favor me da 10 ')
            break
        
        elif escolha not in [1,2,3,4]:
            print('escolha um numero valido! ')




main()