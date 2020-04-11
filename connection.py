#!/usr/lib/python3

from ping3 import ping
import os
import sys
sys.path.insert(1, os.path.abspath("./pyzk"))
from zk import ZK

class DconnTest(ZK):
    internet_add = '8.8.8.8'
    db_srv_add = '10.148.0.3'

    def __init__(self, fg_ip, ovpn_name):
        self.fg_ip = fg_ip
        self.ovpn_name = ovpn_name

    def inet_test(self):
        result = ping(self.internet_add)
        if not result is None:
            print("Internet Connected")
        else:
            print("Internet Disconnected")
        return result

    def vpn_test(self):
        result = ping(self.db_srv_add)
        if not result is None:
            print("VPN Connected")
        else:
            print("VPN Disconnected")
        os.system("systemctl restart openvpn@{}".format(self.ovpn_name))
        print("OpenVPN service has been restart")

    def finger_data(self):
        result = ping(self.fg_ip)
        if not result is None:
            try:
                zk = ZK(self.fg_ip, port=4370, timeout=5, password=0, force_udp=True, ommit_ping=False)
                zk.connect()
                zk.disable_device()
                return zk
            except Exception as e:
                print(e)
        else:
            print("FingerDevice can't ping!")


conn = DconnTest("8.8.8.8")
print(conn.inet_test())
