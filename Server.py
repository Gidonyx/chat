#Выводить ники отправителя
#Убрать Received



import socket, time
import mysql.connector
from threading import Thread

#Каналы
KANALbI = dict()
KANALbI['main_chan'] = list()

#Читаем лог
#serverlog = open('data/serverlog.txt', 'r')
#chtenie = serverlog.read()
#print(chtenie)
#serverlog.close()

#Основной процесс работы
def check_parol_for_login(parol,cnx):
    cursor = cnx.cursor()
    quary = ('select count(*) from users where password ="' + parol + '"')
    cursor.execute(quary)
    for (parol) in cursor:
        parol = parol[0]
        print(parol)
    cursor.close()
    if parol:
        return True
    else:
        return False

def check_login(login,cnx):
    cursor = cnx.cursor()
    quary = ('select count(*) from users where login ="'+login+'"')
    cursor.execute(quary)
    for (login) in cursor:
        login = login[0]
        print(login)
    cursor.close()
    if login:
        return True
    else:
        return False

def new_user(nickname,login,parol,cnx):
    cursor = cnx.cursor()
    quary = ('insert into users (nickname,login,password) values ("'+nickname+'","'+login+'","'+parol+'")')
    cursor.execute(quary)
    appendics = cursor.lastrowid
    cnx.commit()
    cursor.close()

def check_nickname(nickname,cnx):
    cursor = cnx.cursor()
    quary = ('select count(*) from nicknames where nickname ="'+nickname+'"')
    cursor.execute(quary)
    for (nickname) in cursor:
        nickname = nickname[0]
        print(nickname)
    cursor.close()
    if nickname:
        return True
    else:
        return False

def new_nickname(login,nickname,cnx):
    cursor = cnx.cursor()
    quary = ('insert into users (nickname) values ("'+nickname+'") where login = "'+login+'"')
    cursor.execute(quary)
    for (nickname) in cursor:
        print(nickname)
    cnx.commit()
    cursor.close()

def main_process(client_sock, client_addr, cnx):
    chanell = ''
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


        data_dec = data.decode("utf-8")
        data_chan = data.decode("utf-8")
        #Команды сервера

        #Регистрация
        if data_dec.split()[0] == '/create_account':
            login = data_dec.split()[1]
            if check_login(login,cnx):
                client_sock.sendall('Такой логин уже существует'.encode("utf-8"))
            data = client_sock.recv(1024)
            data_dec = data.decode("utf-8")
            parol = data_dec
            new_user(nickname,login,parol,cnx)
            print("Добавлен новый пользователь ")

        #Вход
        if data_dec.split()[0] == '/login':
            login = data_dec.split()[1]
            if check_login(login, cnx):
                client_sock.sendall('Ожидание пароля'.encode("utf-8"))
                data = client_sock.recv(1024)
                data_dec = data.decode("utf-8")
                parol = data_dec
                if check_parol_for_login(parol,cnx):
                    client_sock.sendall('Вход выполнен'.encode("utf-8"))
                else:
                    client_sock.sendall('Ошибка логина - пароля'.encode("utf-8"))



        #Установка ника
        if data_dec.split()[0] == '/set_Nickname':
            nickname = data_dec.split()[1]
            if check_nickname(nickname,cnx):
                client_sock.sendall('Такой пользователь уже существует'.encode("utf-8"))
            new_nickname(nickname, cnx)
        print(vremya, "|", client_addr, "|", nickname, "-", data.decode("utf-8"))



        #Списки каналов
        if data_chan == '/channels':
            print("Запрос информации о каналах")
            for a in KANALbI.keys():
                a+=', '
                client_sock.sendall(a.encode("utf-8"))


        #Создание канала
        if data_chan.split()[0] == '/create_chanell':
            chanell_splitted = data_chan.split()
            chanell = chanell_splitted[1]
            print("Создан канал ", chanell)
            KANALbI[chanell] = list()
            KANALbI[chanell].append(client_sock)
            if client_sock in KANALbI['main_chan']:
                KANALbI['main_chan'].remove(client_sock)
            print('В канал ', chanell, " Вошел ", client_addr, '\n', 'Действующие клиенты', ' ', KANALbI[chanell])

        #Вход на канал
        if data_chan.split()[0] == '/set_chanell':
            chanell_splitted = data_chan.split()
            chanell = chanell_splitted[1]
            print("Подключение", client_addr, "к",  chanell_splitted[1])
            if chanell in KANALbI:
                KANALbI[chanell].append(client_sock)
                print("Подключено в", chanell)
                print('В канал ', chanell, " Вошел ", client_addr, '\n', 'Действующие клиенты', ' ', KANALbI[chanell])
            else:
                client_sock.sendall("Канала не существует".encode("utf-8"))

        if not data:
            break

        if chanell !='':
            for send_sock in KANALbI[chanell]:
                if send_sock != client_sock:
                    send_sock.sendall(data)

#Запуск сервера, сокеты и т.д
def main():
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    serv_sock.bind(('127.0.0.1', 53210))
    serv_sock.listen(10)

    cnx = mysql.connector.connect(user='root', password='rjhdby98',
                                  host='127.0.0.1',
                                  database='chat')
    cursor = cnx.cursor()
    quary = ('delete from nicknames where id !=0')
    cursor.execute(quary)
    appendics = cursor.lastrowid
    cnx.commit()
    cursor.close()

    while True:
        client_sock, client_addr = serv_sock.accept()
        print('Соединено ', client_addr)
        KANALbI['main_chan'].append(client_sock)

        #Многопоточность
        THREAD = Thread(target=main_process, args=(client_sock, client_addr, cnx))
        THREAD.start()
    cnx.close()


if __name__ == "__main__":
    main()