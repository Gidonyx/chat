import socket, time

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('127.0.0.1', 53210))
serv_sock.listen(10)

chanelOne = 0
chanelTwo = 0

clients = []
clients2 = []

serverlog = open('data/serverlog.txt', 'r')
chtenie = serverlog.read()
print(chtenie)
serverlog.close()

while True:
    client_sock, client_addr = serv_sock.accept()
    print('Соединено ', client_addr)

    while True:
        vremya = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        data = client_sock.recv(1024)

        serverlog = open('data/serverlog.txt', 'a')
        serverlog.write(vremya + ' ' + '|' + ' ' + str(data) + '\n')
        serverlog.close()

       # if data == bytes('/set_nickname'.encode()):


        if data == bytes('/set_chanelOne'.encode()):
            clients.append(client_addr)
            print('В первый канал вошел новый клиент', client_addr, '\n', 'Действующие клиенты', ' ', clients)
        if data == bytes('/set_chanelTwo'.encode()):
            clients2.append(client_addr)
            print('Во второй канал вошел новый клиент', client_addr, '\n', 'Действующие клиенты', ' ', clients2)


        print(vremya, "|", client_addr, "-", data)


        if not data:
            break

        if client_addr in clients:
            for i in range(len(clients)):
                client_sock.sendall(data)

        if client_addr in clients2:
            for i in range(len(clients2)):
                client_sock.sendall(data)

        #client_sock.sendall(data)

    client_sock.close()