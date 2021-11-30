# liubenyuan <liubenyuan@gmail.com>
import socket
import network
import time
from machine import Pin


def server_program(host):
    # get the hostname
    # host = "192.168.3.33"
    port = 92  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)

    while True:

        print("waiting for connection")
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))

        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            try:
                data = conn.recv(1024).decode()
                if data == "bye":
                    break
            except OSError:
                print("timeout, disconnect.")
                break
            print("from connected user: " + str(data))
            # data = input(' -> ')
            conn.send(data.encode())  # send data to the client

        conn.close()  # close the connection


if __name__ == "__main__":
    WIFI_LED = Pin(2, Pin.OUT)  # LED
    wlan = network.WLAN(network.STA_IF)  # STA
    wlan.active(True)  # activate
    start_time = time.time()

    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect("firefox", "12345678")  # SSID, PASSWORD

        while not wlan.isconnected():

            # LED Blink
            WIFI_LED.value(1)
            time.sleep_ms(300)
            WIFI_LED.value(0)
            time.sleep_ms(300)

            # Timeout
            if time.time() - start_time > 15:
                print("WIFI Connected Timeout!")
                break

    if wlan.isconnected():
        # LED ON
        WIFI_LED.value(1)
        print("network information:", wlan.ifconfig())

    info = wlan.ifconfig()
    host = info[0]
    print(info[0])

    server_program(host)
