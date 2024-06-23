import re

clientes = dict()
telefoneRegex = re.compile(r'''
    ^                           # Início da string
    (?:\+55\s?)?                # Código do país (opcional): +55
    (?:\(?\d{2}\)?\s?)?         # Código de área com ou sem parênteses e espaço (opcional): (11), (11) , 11 ou 11 
    \d{4,5}                     # Prefixo do telefone (4 ou 5 dígitos): 9999 ou 98888
    -?                          # Hífen (opcional)
    \d{4}                       # Sufixo do telefone (4 dígitos): 8888
    $                           # Fim da string
''', re.VERBOSE)
emailRegex = re.compile(r'''
    ^                           # Início da string
    [a-zA-Z0-9_.+-]+            # Parte local: pode conter letras, números, pontos, sublinhados, sinais de mais e hífens
    @                           # Símbolo @
    [a-zA-Z0-9-]+               # Domínio: pode conter letras, números e hífens
    (\.[a-zA-Z0-9-]+)*          # Domínios de nível superior: podem ter vários segmentos separados por pontos
    \.[a-zA-Z]{2,}              # TLD: deve conter pelo menos duas letras
    $                           # Fim da string
''', re.VERBOSE)


#autoexplicativo
def createCliente(cpf: str, nome: str, telefone: str, email: str):
    c = str(cpf).isdecimal()
    t = telefoneRegex.match(telefone)
    e = emailRegex.match(email)
    if c:
        if t:
            if e:
                clientes.update({cpf : {'cpf':cpf,'nome':nome,'telefone':telefone,'email':email}})
            else:
                print('insira um email valido!')
        else:
            print('insira um telefone valido!')
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
        
        telefone = str(input('qual o telefone? '))
        if telefoneRegex.match(telefone):
            clientes[cpf].update({'telefone':telefone})
        else:
            print('escolha um telefone valido! ')

    elif escolha == 'email':
        email = str(input('qual o email? ')).strip()
        if emailRegex.match(email):
            clientes[cpf].update({'email':email})
        else:
            print('insira um email valido! ')

    else:
        print('escolha uma opcao valida! ')


def deleteCliente(cpf: str):
    try:
        clientes.pop(cpf)
    except:
        print('não existe cliente com esse cpf!')