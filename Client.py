import socket,time

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 53210))

server = ('127.0.0.1', 53210)

chanel = 0

#Выбираем канал
while chanel != '/set_chanelOne' and chanel != '/set_chanelTwo':
    print("Введите команду для выбора канала /set_chanelOne или /set_chanelTwo")
    chanel = input()
client_sock.sendall(chanel.encode())

#Вводим имя
print('Введите имя')
name = input()
client_sock.sendall(name.encode())

while True:

    #Читаем логи
    history = open('data/text.txt', 'r')
    chtenie = history.read()
    print(chtenie)
    history.close()

    #Проверяем на безсимвольность
    print("Введите что-нибудь")
    text = input()
    if len(text) == 0:
        print("В тексте нет ни одного символа")
        continue

    #Запоминаем время и записываем в лог
    vremya_client = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    history = open('data/text.txt', 'a')
    history.write(vremya_client + ' ' + '|' + ' ' + name + ':' + ' ' + text + '\n')
    history.close()

    #Отправляем сообщение
    client_sock.sendall(text.encode())
    data = client_sock.recv(1024)
    print('Received', repr(data))

    #Как закрыть клиент
    if text == 'Exit':
        client_sock.close()
        break




#client_sock.sendall(b'%(clienttext)s'%{"clienttext": text})