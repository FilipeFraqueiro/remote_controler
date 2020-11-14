import pyautogui
import socket
import sys
import os

pyautogui.FAILSAFE = False

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    # ip = "192.168.1.253"

    port = 44444

    address = (ip, port)

    s.bind(address)
    print("Socket started at:", address)

    s.listen(1)

    while True:
        print("Socket listening")
        conn, addr = s.accept()
        print(conn, addr)

        while True:
            data = conn.recv(128)
            data = data.decode()

            if "move\n" in data:
                # print(data)
                
                data = data.replace("move\n", "")
                data = data.split(",")
                
                x = float(data[0])
                y = float(data[1])
                # print(x, y)
                pyautogui.move(x, -y)

            elif "touch" in data:
                # print(data)
                pyautogui.click()

            else:
                # print(data)
                pyautogui.press(data)

            if not data:
                conn.close()
                print("Connection closed\n\n")
                break



if __name__ == '__main__':
    main()
    # try:
    #     main()

    # except KeyboardInterrupt:
    #     s.close()
    #     print('Interrupted')
    #     try:
    #         sys.exit(0)
    #     except SystemExit:
    #         os._exit(0)

