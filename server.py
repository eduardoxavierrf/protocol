from socket import (AF_INET, SOCK_STREAM, socket)

grades = {}

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', 8080))
serverSocket.listen(1)
print('Server started on port 8080 🚀')
while True:
    connectionSocket, addr = serverSocket.accept()

    request = connectionSocket.recv(1024)
    
    request = request.decode("utf-8")
    request = request.split('|')
    if (request[0] == 'professor'):
        if request[2] == 'baixar trabalho':
            file = open('trabalho_' + request[1] + '.pdf', 'rb')
            file_bytes = file.read(1024)

            while file_bytes:
                connectionSocket.send(file_bytes)
                file_bytes = file.read(1024)
            file.close()
        elif request[2] == 'enviar nota':
            grades[request[1]] = request[3]

    elif (request[0] == 'aluno'):
        if request[2] == 'send file':
            f = open('trabalho_' + request[1] + '.pdf','wb')
            file_bytes = connectionSocket.recv(1024)
            while file_bytes:
                f.write(file_bytes)
                file_bytes = connectionSocket.recv(1024)
            f.close()
            
        elif request[2] == 'consultar nota':
            if grades.get(request[1]) == None:
                connectionSocket.send('Sem nota disponivel'.encode())
            else:
                connectionSocket.send(grades.get(request[1]).encode())
    connectionSocket.close()