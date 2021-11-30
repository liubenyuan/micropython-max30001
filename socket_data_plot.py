# liubenyuan <liubenyuan@gmail.com>
import numpy as np
import matplotlib.pyplot as plt
import socket
import struct
import time


def send_msg(skt, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack("I", len(msg)) + msg
    skt.sendall(msg)


def recv_msg(skt):
    # Read message length and unpack it into an integer
    raw_msglen = skt.recv(4)
    if not raw_msglen:
        return None
    msglen = struct.unpack("I", raw_msglen)[0]
    return recvall(skt, msglen)


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)

    return data


# create canvas
n = 256
x = np.linspace(0, 10, n)
y = np.zeros_like(x)

plt.ion()
figure, ax = plt.subplots(figsize=(8, 6))
(line1,) = ax.plot(x, y)
ax.grid(True)

plt.title("Dynamic Plot of BIOZ", fontsize=21, fontweight="bold")
plt.xlabel("time", fontsize=15)
plt.ylabel("bioz (micro Ohms)", fontsize=15)

# main program
host = "192.168.3.11"
port = 92
client_socket = socket.socket()
client_socket.connect((host, port))

message = "bioz"
while 1:
    send_msg(client_socket, message.encode())
    rx = recv_msg(client_socket)
    size = len(rx)
    data_size = size // 4  # float, if you are using short, 4 -> 2
    print("Received from server: {}".format(size))
    d = np.array(struct.unpack(">{}f".format(data_size), rx))

    y = np.concatenate([y, d])[-n:]
    line1.set_ydata(y)
    ymin, ymax = np.min(y), np.max(y)
    ax.set_ylim([ymin, ymax])
    figure.canvas.draw()
    figure.canvas.flush_events()
    time.sleep(0.1)

client_socket.close()  # close the connection
