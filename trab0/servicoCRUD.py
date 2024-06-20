servico = list()
id = 0


def createServico(cpf: str, valor: float, status: str):
    servico.append({'cpf':cpf,'valor':valor,'status':status})
    id += 1


def deleteServico(ID):
    try:
        servico.pop(ID)
        id-=1
    except:
        print('insira um ID valido!')


def readServico(ID):
    try:
        print(servico[ID])
    except:
        print('insira um ID valido!')

#def updateServico(ID):



