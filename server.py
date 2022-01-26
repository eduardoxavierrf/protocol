from socket import (AF_INET, SOCK_STREAM, socket)

grades = {}

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', 8080))
serverSocket.listen(1)
print('Server started on port 8080 🚀')
while True:
    connectionSocket, addr = serverSocket.accept()
    f = open('server_file' + '.pdf','wb')
    file_bytes = connectionSocket.recv(1024)
    while file_bytes:
        f.write(file_bytes)
        file_bytes = connectionSocket.recv(1024)
    f.close()
    # request = request.decode("utf-8")
    # request = request.split('|')
    # if (request[0] == 'professor'):
    #     grades[request[1]] = request[2]
    # elif (request[0] == 'aluno'):
    #     if grades.get(request[1]) == None:
    #         connectionSocket.send('Sem nota disponivel'.encode())
    #     else:
    #         connectionSocket.send(grades.get(request[1]).encode())
    connectionSocket.close()