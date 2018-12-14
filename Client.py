import socket,time
from threading import Thread

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('192.168.88.91', 53210))

server = ('192.168.88.91', 53210)



def listen_Server():
    while True:
        try:
            data = client_sock.recv(1024)
            print('Received', repr(data.decode("utf-8")))
        except Exception:
            print('Socket close')
            return

def main():

    THREAD = Thread(target=listen_Server)
    THREAD.start()

    #Создаем канал
    print("Для создания канала введите /create_chanell НАЗВАНИЕ")

    # Создаем канал
    print("Список уже существующих каналов можно посмотреть при помощи команды /channels")

    #Подключение
    print("Для подключения к уже существующему каналу введите /set_chanell НАЗВАНИЕ")

    account=''

    print("Введите /create_account ЛОГИН для регистрации или /login ЛОГИН для входа")
    login, check = "", ""
    while check != '/create_account' and check != '/login':
        login = input()
        check = login.split()[0]
        if check == '/create_account':
            client_sock.sendall(login.encode())
            print ("Введите пароль")
            parol = input()
            print("Повторите пароль")
            parol_povtor = input()
            if parol == parol_povtor:
                client_sock.sendall(parol.encode())
            else:
                continue
        if check == '/login':
            client_sock.sendall(login.encode())
            print('Введите пароль')
            parol_login = input()
            client_sock.sendall(parol_login.encode())


    print("Введите ник /set_Nickname <nickname>")
    nickname, check = "",""
    while check != '/set_Nickname':
        nickname = input()
        check = nickname.split()[0]
    client_sock.sendall(nickname.encode())

    while True:
        #Читаем логи
     #   history = open('data/text.txt', 'r')
     #   print(history.read())
     #   history.close()

        #Проверяем на безсимвольность
        print("Введите что-нибудь")
        text = input()
        if len(text) == 0:
            print("В тексте нет ни одного символа")
            continue
        if text.split()[0] == '/create_chanel':
            print("Создан канал с названием ", text.split()[1])

        #Запоминаем время и записываем в лог
        vremya_client = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        history = open('data/text.txt', 'a')
        history.write(vremya_client + ' ' + '|' + ' ' + nickname.split()[1] + ':' + ' ' + text + '\n')
        history.close()

        #Отправляем сообщение
        client_sock.sendall(text.encode())

        #Как закрыть клиент
        if text == 'Exit':
            client_sock.close()
            break
if __name__ == "__main__":
    main()