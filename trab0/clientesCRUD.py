clientes = dict()

#autoexplicativo
def setCliente(cpf: str, nome: str, telefone: int, email:str):
    clientes.update({cpf : {'cpf':cpf,'nome':nome,'telefone':telefone,'email':email}})

def delCliente(cpf: str):
    try:
        clientes.pop(cpf)
    except:
        print('não existe cliente com esse cpf!')

def readCliente(cpf):
    try:
        c = clientes.get(cpf)
        print(c)
    except:
        print('não existe cliente com esse cpf!')

