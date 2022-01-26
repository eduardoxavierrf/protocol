from math import ceil
from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('localhost', 8080))

role = input('Qual é seu cargo?<aluno/professor> ')

if (role == 'professor'):
    studentName = input('Digite o nome do aluno: ')

    wantTo = input('O que você quer fazer?<enviar nota/baixar trabalho> ')

    if wantTo == 'enviar nota':
        grade = input('Digite a nota do aluno: ')
        request = role + '|' + studentName + '|' + 'enviar nota' + '|' + grade
        clientSocket.send(request.encode())
        print('A nota foi enviada com sucesso')

    elif wantTo == 'baixar trabalho':
        request = role + '|' + studentName + '|' + 'baixar trabalho'
        clientSocket.send(request.encode())
        f = open('trabalhos_recebidos/' + 'trabalho_' + studentName + '.pdf','wb')
        file_bytes = clientSocket.recv(1024)
        while file_bytes:
            f.write(file_bytes)
            file_bytes = clientSocket.recv(1024)
        f.close()

    clientSocket.close()

elif (role == 'aluno'):
    studentName = input('Digite o seu nome: ')

    wantTo = input(studentName + ' o que você quer fazer?<consultar nota/enviar trabalho> ')

    if wantTo == 'consultar nota':
        request = role + '|' + studentName + '|' + 'consultar nota'
        clientSocket.send(request.encode())
        grade = clientSocket.recv(1024)
        print('Nota: ', grade)
    elif wantTo == 'enviar trabalho':
        path = input('Digite o caminho até o arquivo do trabalho (Deve ser um PDF): ')

        request = role + '|' + studentName + '|' + 'send file'
        clientSocket.send(request.encode())
        file = open(path, 'rb')
        
        file_bytes = file.read(1024)

        while file_bytes:
            clientSocket.send(file_bytes)
            file_bytes = file.read(1024)
        file.close()

        print('Trabalho enviado')
    
    
    clientSocket.close()