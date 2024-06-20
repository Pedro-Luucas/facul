clientes = dict()

#autoexplicativo
def createCliente(cpf: str, nome: str, telefone: int, email: str):
    c = str(cpf).isdecimal()
    if c:
        clientes.update({cpf : {'cpf':cpf,'nome':nome,'telefone':telefone,'email':email}})
    else:
        print('insira um cpf valido! ')
        

def readCliente(cpf: str):
    try:
        c = clientes.get(cpf)
        print(c)
    except:
        print('não existe cliente com esse cpf!')


def updateClientes(cpf: str):
    escolha = str(input('qual campo você quer mudar? (nome, telefone, email)')).lower().strip()

    if escolha == 'nome':
        nome = str(input('qual o nome? ')).title().strip()
        clientes[cpf].update({'nome':nome})

    elif escolha == 'telefone':
        try:
            telefone = int(input('qual o telefone? '))
            clientes[cpf].update({'telefone':telefone})
        except:
            print('escolha um telefone valido (somente os digitos) ')

    elif escolha == 'email':
        email = str(input('qual o email? ')).strip()
        clientes[cpf].update({'email':email})


def deleteCliente(cpf: str):
    try:
        clientes.pop(cpf)
    except:
        print('não existe cliente com esse cpf!')