import socket


def server_program():
    # get the hostname
    host = "192.168.3.11"
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
        conn.settimeout(None)

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
    server_program()
