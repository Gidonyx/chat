import asyncio

users = []


async def handle(reader, writer):
    addr = writer.get_extra_info('peername')
    message = f"{addr!r} подключился !!!!"
    print(message)
    users.append(writer)
    for writer in users:
        writer.write(b"Hello")
        await writer.drain()
    while True:
        data = await reader.read(1024)
        message = data.decode().strip()
        print(data)
        writer.write(data)
        await writer.drain()
        if message == "exit":
            message = f"{addr!r} закрыл соединение."
            print(message)
            break
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Подключен на {addr}')
    async with server:
        await server.serve_forever()

asyncio.run(main())