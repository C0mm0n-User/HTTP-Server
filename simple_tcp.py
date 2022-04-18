import socket


serv_sock = socket.socket(socket.AF_INET,      # Задаем семейство протоколов 'Интернет' (INET)
                          socket.SOCK_STREAM,  # Задаем тип передачи данных 'потоковый' (TCP)
                          proto=0)             # Выбираем протокол 'по умолчанию' для TCP, т.е. IP
serv_sock.bind(('', 53212))  # привязываем созданный сокет к сетевому адаптору (ip + port)
serv_sock.listen(5) # переводим сокет в состояние ожидания подключения, сообщив об этом ОС

while True:
    # Бесконечно обрабатываем входящие подключения
    client_sock, client_addr = serv_sock.accept()
    print('Connected by', client_addr)

    while True:
        # Пока клиент не отключился, читаем передаваемые
        # им данные и отправляем их обратно
        data = client_sock.recv(1024)
        if not data:
            # Клиент отключился
            break
        print(data)
        client_sock.sendall(b'hello')

    client_sock.close()

#  telnet 127.0.0.1 53210 ; 'ctrl + ]', then 'quit' to exit
