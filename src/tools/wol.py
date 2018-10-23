import struct
import sys
import socket

def to_hex_int(s):
    return int(s.upper(), 16)

def wolrun(mac,ip):
    ip_prefix = '.'.join(ip.split('.')[:-1]) 
    destip =ip = '%s.%s'%(ip_prefix,'255')
    print destip 
    dest = (destip, 9)
    spliter = ""
    if mac.count(":") == 5: spliter = ":"
    if mac.count("-") == 5: spliter = "-"
    if spliter == "":
        print("MAC address should be like XX:XX:XX:XX:XX:XX / XX-XX-XX-XX-XX-XX")
        return False

    parts = mac.split(spliter)
    a1 = to_hex_int(parts[0])
    a2 = to_hex_int(parts[1])  
    a3 = to_hex_int(parts[2])
    a4 = to_hex_int(parts[3])
    a5 = to_hex_int(parts[4])
    a6 = to_hex_int(parts[5])
    addr = [a1, a2, a3, a4, a5, a6]

    packet = chr(255) + chr(255) + chr(255) + chr(255) + chr(255) + chr(255)

    for n in range(0,16):
        for a in addr:
            packet = packet + chr(a)

    packet = packet + chr(0) + chr(0) + chr(0) + chr(0) + chr(0) + chr(0)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    s.sendto(packet,dest)

    print("WOL packet %d bytes sent !" % len(packet))
    return True
if __name__ == "__main__": 
    #wolrun('00-23-7d-c7-a5-44','10.13.28.202')
    wolrun('00-1f-c6-ac-ec-ec','10.13.28.69')
    #wolrun('00-23-7d-c7-9a-a4','10.13.28.140')
    #wolrun('2c:60:0c:52:81:ce','172.0.19.125')


