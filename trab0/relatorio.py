import clientesCRUD
import servicoCRUD


def gerarRelatorio():
    print('-*'*15)
    print('relatorio dos clientes abaixo:\n')

    for key, value in clientesCRUD.clientes.items():
        print(value)

    print('\n','-*'*15)
    print('--'*15)
    print('-*'*15)
    print('relatorio das ordens de servico abaixo: \n')

    for key, value in servicoCRUD.servico.items():
        print(value)

    print('\n','-*'*15)
    print('relatorio finalizado! ')
