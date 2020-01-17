import socket
import queue
import threading

class Client:
    def __init__(self):
        self.send_queue = queue.Queue()
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(('localhost',9292))
        self.recv = threading.Thread(target=self._recv)
        self.recv.start()
        self._send()

    def _recv(self):
        while True:
            data = self.client.recv(1024)
            if data:
                print("\rSERVER:\t" + str(data.decode()),flush=True)
                print("CLIENT:\t", end=" ")

    def _send(self):
        while True:
            msg = input("CLIENT:\t")
            if msg.lower() == "exit" or msg == "":
                self.client.close()
                break
            else:
                self.client.sendall(msg.encode())


if __name__ == "__main__":
    Client()