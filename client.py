from math import ceil
from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('localhost', 8080))

role = input('Qual é seu cargo?<aluno/professor> ')

if (role == 'professor'):
    studentName = input('Digite o nome do aluno: ')
    grade = input('Digite a nota do aluno: ')
    request = role + '|' + studentName + '|' + grade
    clientSocket.send(request.encode())
    print('A nota foi enviada com sucesso')
    clientSocket.close()
elif (role == 'aluno'):
    studentName = input('Digite o seu nome: ')

    wantTo = input(studentName + ' o que você quer fazer?<consultar nota/enviar trabalho> ')

    if wantTo == 'consultar nota':
        request = role + '|' + studentName + '|' + ''
        clientSocket.send(request.encode())
        grade = clientSocket.recv(1024)
        print('Nota: ', grade)
    elif wantTo == 'enviar trabalho':
        request = role + '|' + studentName + '|' + 'send file'
        clientSocket.send(request.encode())
        file = open('trabalho/boa.pdf', 'rb')
        
        file_bytes = file.read(1024)

        while file_bytes:
            clientSocket.send(file_bytes)
            file_bytes = file.read(1024)
        file.close()

        print('Trabalho enviado')
    
    
    clientSocket.close()