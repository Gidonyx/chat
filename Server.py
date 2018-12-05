import socket, time
from threading import Thread

#Каналы



KANALbI = dict()
KANALbI['main_chan']=list()


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

        try:
            data = client_sock.recv(1024)
        except Exception:
            client_sock.close()
            print('Socket Closed ', client_addr)
            return


        #Пишем в лог
        serverlog = open('data/serverlog.txt', 'a')
        serverlog.write(vremya + ' ' + '|' + ' ' + str(data) + '\n')
        serverlog.close()

        #Команды сервера
        data_dec = data.decode("utf-8")
        data_chan = data.decode("utf-8")


        if data_dec.split()[0] == '/set_Nickname':
            nickname = data_dec.split()[1]
        print(vremya, "|", client_addr, "|", nickname, "-", data.decode("utf-8"))

        chanell=''
        chanell_splitted = data_chan.split()


        if chanell_splitted[0] == '/create_chanel':
            chanell = chanell_splitted[1]
            print("Создан канал ", chanell)
            KANALbI[chanell] = list()
            KANALbI[chanell].append(client_sock)
            if client_sock in  KANALbI['main_chan']:
                KANALbI['main_chan'].remove(client_sock)
            print('В канал ',chanell , " Вошел " , client_addr, '\n', 'Действующие клиенты', ' ', KANALbI[chanell])


        if not data:
            break

        if chanell !='':
            for send_sock in KANALbI[chanell]:
                if send_sock != client_sock:
                    send_sock.sock.sendall(data)

#Запуск сервера, сокеты и т.д
def main():
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    serv_sock.bind(('127.0.0.1', 53210))
    serv_sock.listen(10)

    while True:
        client_sock, client_addr = serv_sock.accept()
        print('Соединено ', client_addr)
        KANALbI['main_chan'].append(client_sock)

        #Многопоточность
        THREAD = Thread(target=main_process, args=(client_sock, client_addr))
        THREAD.start()

if __name__ == "__main__":
    main()