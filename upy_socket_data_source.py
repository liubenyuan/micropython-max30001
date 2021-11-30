# liubenyuan <liubenyuan@gmail.com>
import network
import time
from machine import Pin
import socket
import struct
import random


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


def server_program(host):
    port = 92
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)

    while True:

        print("waiting for client")
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        conn.settimeout(5)

        while True:
            try:
                rx = recv_msg(conn).decode()
            except OSError:
                print("socket timeout, disconnect.")
                break
            print("user: " + str(rx))

            # [MAX30001] replace d with your BIOZ data !
            buf_len = 10
            d = []
            for i in range(buf_len):
                d.append(random.random())
            d_bytes = struct.pack(">{}f".format(buf_len), *d)
            send_msg(conn, d_bytes)

        conn.close()


if __name__ == "__main__":

    WIFI_LED = Pin(2, Pin.OUT)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    start_time = time.time()

    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect("firefox", "12345678")

        while not wlan.isconnected():
            WIFI_LED.value(1)
            time.sleep_ms(300)
            WIFI_LED.value(0)
            time.sleep_ms(300)

            # Time out
            if time.time() - start_time > 15:
                print("WIFI Connected Timeout!")
                break

    if wlan.isconnected():
        WIFI_LED.value(1)
        print("network information:", wlan.ifconfig())

    info = wlan.ifconfig()
    host = info[0]
    print("host IP = ", host)
    server_program(host)
