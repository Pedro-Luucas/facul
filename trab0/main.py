from clientesCRUD import *
from servicoCRUD import *

def main():
    while True:
        print('-*'*15)
        escolha = int(input('voce quer editar um cliente ou uma ordem de servico? \n(1 para cliente, 2 para ordem de servico) '))
        if escolha == 1:
            subEscolha = int(input("""1 para cadastrar novo cliente\n
                                   2 para ver as informacoes do cliente\n
                                   3 para editar alguma informação do cliente\n
                                   4 para deletar algum cliente """))
            match subEscolha:
                case 1:
                    cpf = str(input('qual o cpf do cliente? '))
                    nome = str(input('qual o nome do cliente? '))
                    telefone = int(input('qual o telefone do cliente? (somente os digitos) '))
                    email = str(input('qual o email do cliente?'))
                    createCliente(cpf, nome, telefone, email)

                case 2:
                    cpf = str(input('qual o cpf do cliente?'))
                    readCliente(cpf)

                case 3:
                    cpf = str(input('qual o cpf do cliente?'))
                    updateClientes(cpf)

                case 4:
                    cpf = str(input('qual o cpf do cliente?'))
                    deleteCliente(cpf)
                case _:
                    print('escolha um numero valido!')
                    continue

        elif escolha == 2:
            subEscolha = int(input("""1 para cadastrar nova ordem de servico\n
                                   2 para ver as informacoes da ordem de servico\n
                                   3 para editar alguma informação da ordem de servico\n
                                   4 para deletar alguma ordem de servico """))
            match subEscolha:
                case 1:
                    cpf = str(input('qual o cpf do cliente? '))
                    valor = float(input('qual o valor da ordem? '))
                    status = str('qual o status da ordem?')
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


