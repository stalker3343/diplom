import random
import socket
import struct


def CVE_2020_0796(target: str, gradation):
    # pkt = open("./packet.txt", "r").read().encode()
    from django.conf import settings
    # pkt = open(str(settings.BASE_DIR) + '/main/tasks/SambaVuln/packet.txt', "r").read().encode()
    pkt = b'\x00\x00\x00\xc0\xfeSMB@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x00\x08\x00\x01\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00x\x00\x00\x00\x02\x00\x00\x00\x02\x02\x10\x02"\x02$\x02\x00\x03\x02\x03\x10\x03\x11\x03\x00\x00\x00\x00\x01\x00&\x00\x00\x00\x00\x00\x01\x00 \x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\n\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'

    sock = socket.socket(socket.AF_INET)
    sock.settimeout(3)
    # if gradation:
    #     log_info(f"Checking if {target} is vulnerable...")
    #     result = random.randint(1, 2)
    #     log_success(f"{target} Not vulnerable.") if result == 1 else log_error(f"{target} vulnerable.")
    #     return result
    try:
        sock.connect((str(target),  445))

        sock.send(pkt)
        nb, = struct.unpack(">I", sock.recv(4))
        res = sock.recv(nb)
        log_success(f"{target} Not vulnerable.") if res[68:70] != b"\x11\x03" or res[70:72] != b"\x02\x00" else log_error(f"{target} vulnerable.")
        
        return 2 if res[68:70] != b"\x11\x03" or res[70:72] != b"\x02\x00" else 1

        #return f"{target} Not vulnerable." if res[68:70] != b"\x11\x03" or res[70:72] != b"\x02\x00" \
        #    else f"{target} Vulnerable"
    # except ValueError as e:
    #     print("Сведения об исключении", e)
    #     return f"Connect to host {target} unreachable"
    finally:
        sock.close()


def log_info(s):
    print(f"\033[96m[*] {s}\033[0m")


def log_success(s):
    print(f"\033[92m[+] {s}\033[0m")


def log_error(s):
    print(f"\033[91m[-] {s}\033[0m")

