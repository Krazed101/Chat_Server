import socket
import select
import queue

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost', 9292))
server.listen(5)
inputs = [server]
outputs = []
message_queues = {}

while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    for conn in readable:
        print(str(conn) + " in Readable")
        if conn is server:
            connection, client_address = conn.accept()
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            data = conn.recv(1024)
            print("Data Received")
            if data or str(data.decode()).lower() != "exit":
                print("Data Exists and isn't exit")
                for c in inputs:
                    print(c)
                    if c != conn and c != server:
                        print("Adding Connection to Output")
                        message_queues[c].put_nowait(data)
                        outputs.append(c)
            else:
                if conn in outputs:
                    outputs.remove(conn)
                inputs.remove(conn)
                conn.close()
                del message_queues[conn]

    for conn in writable:
        print(str(conn) + " in Writable")
        try:
            next_msg = message_queues[conn].get_nowait()
        except queue.Empty:
            outputs.remove(conn)
        else:
            conn.sendall(next_msg)

    for conn in exceptional:
        print(str(conn) + " in Exceptional")
        inputs.remove(conn)
        if conn in outputs:
            outputs.remove(conn)
        conn.close()
        del message_queues[conn]