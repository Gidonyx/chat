import socket,time
from threading import Thread

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 53210))

server = ('127.0.0.1', 53210)



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
    print ("Для создания канала введите /create_chanel НАЗВАНИЕ")

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