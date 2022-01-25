from socket import *
from urllib import request

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
    request = role + '|' + studentName + '|' + ''
    clientSocket.send(request.encode())
    modifiedSentence = clientSocket.recv(1024)
    print('Nota: ', modifiedSentence)
    clientSocket.close()