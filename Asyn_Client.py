import asyncio
import socket,time
from threading import Thread

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 8888))

def listen_Server():
    while True:
        try:
            data = client_sock.recv(1024)
            print(repr(data.decode("utf-8")))
        except Exception:
            print('Socket close')
            return

def main():
    THREAD = Thread(target=listen_Server)
    THREAD.start()

while True:
    print("Введите что-нибудь")
    text = input()
    if len(text) == 0:
        print("В тексте нет ни одного символа")
        continue

    vremya_client = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Отправляем сообщение
    client_sock.send(text.encode())

    # Как закрыть клиент
    if text == 'Exit':
        client_sock.close()
        break


if __name__ == "__main__":
    main()

