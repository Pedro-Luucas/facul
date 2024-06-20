from random import randint
servico = list()
ids = list()

def createServico(cpf: str, valor: float, status: str):
    servico.append({'cpf':cpf,'valor':valor,'status':status})
    while True:
        id = randint(0,9999)
        if id not in ids:
            ids.append(id)
            break
        else:
            continue
    print(f'o ID dessa ordem é {id}')
    


def deleteServico(ID):
    try:
        servico.pop(ID)
    except:
        print('insira um ID valido!')


def readServico(ID):
    try:
        print(servico[ID])
    except:
        print('insira um ID valido!')


def updateServico(ID):
    escolha = str(input('qual campo você quer mudar? (valor, status)')).lower().strip()
        
    if escolha == 'valor':
        valor = str(input('qual o valor? ')).title().strip()
        servico[ID].update({'valor':valor})
    
    elif escolha == 'status':
        status = str(input('qual o status? ')).title().strip()
        servico[ID].update({'status':status})



