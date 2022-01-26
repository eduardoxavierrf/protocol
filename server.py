from socket import (AF_INET, SOCK_STREAM, socket)

class Request:
    def __init__(self, request):
        request = request.decode("utf-8")
        request = request.split('|')
        self.role = request[0]
        self.studentName = request[1]
        self.action = request[2]
        self.arg = request[3] if 3 < len(request) else None

grades = {}

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', 8080))
serverSocket.listen(1)
print('Server started on port 8080 🚀')
while True:
    connectionSocket, addr = serverSocket.accept()

    request = Request(connectionSocket.recv(1024))

    if (request.role == 'professor'):
        if request.action == 'baixar trabalho':
            file = open('trabalho_' + request.studentName + '.pdf', 'rb')
            file_bytes = file.read(1024)

            while file_bytes:
                connectionSocket.send(file_bytes)
                file_bytes = file.read(1024)
            file.close()
        elif request.action == 'enviar nota':
            grades[request.studentName] = request.arg

    elif (request.role == 'aluno'):
        if request.action == 'send file':
            f = open('trabalho_' + request.studentName + '.pdf','wb')
            file_bytes = connectionSocket.recv(1024)
            while file_bytes:
                f.write(file_bytes)
                file_bytes = connectionSocket.recv(1024)
            f.close()

        elif request.action == 'consultar nota':
            if grades.get(request.studentName) == None:
                connectionSocket.send('Sem nota disponivel'.encode())
            else:
                connectionSocket.send(grades.get(request.studentName).encode())
    connectionSocket.close()