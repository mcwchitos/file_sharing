import sys, os
import socket
from threading import Thread

HOST = ""


def append_suffix(file_name: str, n):
    if '.' in file_name:
        file_without_ext = "".join(file_name.split(".")[:-1])
        extension = file_name.split(".")[-1]
        return f"{file_without_ext}_copy{n}.{extension}"
    else:
        return f"{file_name}_copy{n}"


def get_formatted_filename(file_name):
    if os.path.exists(file_name):
        i = 1
        while True:
            new_file_name = append_suffix(file_name, i)
            if os.path.exists(new_file_name):
                i += 1
            else:
                return new_file_name
    return file_name


def receive_file(conn, address):
    with conn:
        print(f"Receiving a file from {address}")
        # receive a filename size and a filename itself
        file_name_size = int.from_bytes(conn.recv(1), 'big')
        file_name = (conn.recv(file_name_size)).decode()
        # change a filename if it already exists
        file_name = get_formatted_filename(file_name)
        # receive bytes of a file and write them to a local file
        with open(file_name, "wb") as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"The file was received and saved with '{file_name}' name")


if __name__ == "__main__":
    port = int(sys.argv[1])
    # establish a socket and listen to connection attempts
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        while True:
            s.listen(1)
            conn, address = s.accept()
            # create a separate thread for handling a connection from a client
            thread = Thread(target=receive_file, args=(conn, address))
            thread.start()