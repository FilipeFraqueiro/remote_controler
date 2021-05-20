import pyautogui
import socket
import sys
import os

pyautogui.FAILSAFE = False

def main(ip):
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
                
                try:
                    x = float(data[0])
                    y = float(data[1])
                    # print(x, y)
                    pyautogui.move(x, -y)
                    
                except Exception as e:
                    pass
                    # print("failed to move")

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
    ip = input("Enter local IP addres: ")
    main(ip)

