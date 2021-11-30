# liubenyuan <liubenyuan@gmail.com>
import numpy as np
import socket
import struct


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


def server_program():
    # get the hostname
    host = "192.168.3.11"
    port = 92

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)

    while True:

        print("waiting for connection.")
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        conn.settimeout(5)

        while True:
            try:
                rx = recv_msg(conn).decode()
            except OSError:
                print("timeout, disconnect")
                break
            print("user: " + str(rx))

            # replace d with your BIOZ data !
            buf_len = 10
            d = np.random.randn(buf_len).astype(np.float32)
            d_bytes = struct.pack(">{}f".format(buf_len), *d)
            send_msg(conn, d_bytes)

        conn.close()  # close the connection


if __name__ == "__main__":
    server_program()
