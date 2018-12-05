import socket, time
from threading import Thread

#Каналы
channel = []
channel2 = []

KANALbI = dict()


#Читаем лог
#serverlog = open('data/serverlog.txt', 'r')
#chtenie = serverlog.read()
#print(chtenie)
#serverlog.close()

#Основной процесс работы
def main_process(client_sock, client_addr):
    nickname = ''
    while True:
        vremya = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        data = client_sock.recv(1024)

        #Пишем в лог
        serverlog = open('data/serverlog.txt', 'a')
        serverlog.write(vremya + ' ' + '|' + ' ' + str(data) + '\n')
        serverlog.close()

        #Команды сервера
        data_dec = data.decode("utf-8")
        data_chan = data.decode("utf-8")

        if data == bytes('/set_chanelOne'.encode()):
            channel.append(client_sock)
            print('В первый канал вошел новый клиент', client_addr, '\n', 'Действующие клиенты', ' ', channel)
        if data == bytes('/set_chanelTwo'.encode()):
            channel2.append(client_sock)
            print('Во второй канал вошел новый клиент', client_addr, '\n', 'Действующие клиенты', ' ', channel2)
        if data_dec.split()[0] == '/set_Nickname':
            nickname = data_dec.split()[1]
        print(vremya, "|", client_addr, "|", nickname, "-", data.decode("utf-8"))
        if data_chan.split()[0] == '/create_chanel':
            chanell = data_chan.split()[1]
            print("Создан канал ", chanell)
            KANALbI[chanell] = list()
            KANALbI[chanell].append(client_sock)
            print('В канал ',chanell , " Вошел " , client_addr, '\n', 'Действующие клиенты', ' ', KANALbI[chanell])


        if not data:
            break

        for chanell0, spiski in KANALbI.items():
            flag = 0
            for ip in spiski:
                if ip == client_sock:
                    for ip in KANALbI[chanell0]:
                        if ip != client_sock:
                            ip.sock.sendall(data)
                    flag = 1
                    break
            if flag == 1:
                break

        #Отправка по каналам
        if client_sock in channel:
            for channel_sock in channel:
                if channel_sock != client_sock:      #интересная строка - она отвечает за то, чтобы отправитель не получал собственные сообщения
                    channel_sock.sendall(data)

        if client_sock in channel2:
           for channel_sock in channel2:
               if channel_sock != client_sock:       #интересная строка - она отвечает за то, чтобы отправитель не получал собственные сообщения
                   channel_sock.sendall(data)

#Запуск сервера, сокеты и т.д
def main():
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    serv_sock.bind(('127.0.0.1', 53210))
    serv_sock.listen(10)

    while True:
        client_sock, client_addr = serv_sock.accept()
        print('Соединено ', client_addr)

        #Многопоточность
        THREAD = Thread(target=main_process, args=(client_sock, client_addr))
        THREAD.start()

if __name__ == "__main__":
    main()