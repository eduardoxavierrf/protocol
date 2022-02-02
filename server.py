from socket import (AF_INET, SOCK_STREAM, socket)
import sqlite3

class Request:
    def __init__(self, request: bytes) -> None:
        request = request.decode("utf-8")
        request = request.split('|')
        self.role = request[0]
        self.studentName = request[1]
        self.action = request[2]
        self.arg = request[3] if 3 < len(request) else None

grades = {}

try:
    # connect to db
    conn = sqlite3.connect('server.db')
    cur = conn.cursor()

    # create grades table if dont exists
    cur.execute('CREATE TABLE IF NOT EXISTS grades (student_name text, grade real)')
    conn.commit()

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
                request.arg = float(request.arg)
                cur.execute('INSERT INTO grades (student_name, grade) VALUES (?, ?)', (request.studentName, request.arg))
                conn.commit()

        elif (request.role == 'aluno'):
            if request.action == 'send file':
                f = open('trabalho_' + request.studentName + '.pdf','wb')
                file_bytes = connectionSocket.recv(1024)
                while file_bytes:
                    f.write(file_bytes)
                    file_bytes = connectionSocket.recv(1024)
                f.close()

            elif request.action == 'consultar nota':
                cur.execute('SELECT * FROM grades WHERE student_name=?', (request.studentName,))
                if cur.fetchone() == None:
                    connectionSocket.send('Sem nota'.encode())
                else:
                    connectionSocket.send(str(cur.fetchone()[1]).encode())
        connectionSocket.close()
except Exception as e:
    print('\nClosing server connection...')
    conn.close()
    serverSocket.close()