import sys, os
import socket
from threading import Thread


def send_file(filename, address, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((address, port))
        if os.path.isfile(filename):
            # send size of a filename and the filename itself
            s.sendall(len(filename).to_bytes(1, 'big'))
            s.sendall(str(filename).encode())
            # the size of a file used for percentage bar
            file_size = os.path.getsize(filename)
            send_size = 0
            with open(filename, "rb") as file:
                while True:
                    sys.stdout.write("\r")
                    sys.stdout.write(f"{send_size} of {file_size} bytes sent - {send_size * 100 / file_size :.2f}% done")
                    sys.stdout.flush()
                    # read at most 1024 bytes of a file if not EOF
                    buf = file.read(1024)
                    if not buf:
                        break
                    # send bytes through socket
                    s.sendall(buf)
                    send_size += len(buf)
            print()
            print("File has been send")
        else:
            print("This is not a file!")


if __name__ == "__main__":
    args = sys.argv[1:]
    filename, address, port = args
    # create a separate thread for sending a file
    thread = Thread(target=send_file, args=(filename, address, int(port)))
    thread.start()
    thread.join()