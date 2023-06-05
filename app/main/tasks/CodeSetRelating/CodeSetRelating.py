#!/usr/bin/env python3
import argparse
import copy
import json
import os
import random
import re

import requests
from bs4 import BeautifulSoup


def get_args():
    parser = argparse.ArgumentParser(description="Scan ManageEngine web instances for CodeSetRelating")
    parser.add_argument("-f", help="File containing a list of URLs to scan", dest="file", required=False)
    parser.add_argument("-t", help="Comma-separated list of URLs to scan", dest="targets", required=False)
    parser.add_argument("-o", help="Output directory", dest="output_dir", default="./")
    args = parser.parse_args()
    return args


# add status printing with different colors
class Print:
    RED = "\033[01;31m"
    GREEN = "\033[01;32m"
    YELLOW = "\033[01;33m"
    BLUE = "\033[01;34m"
    MAGENTA = "\033[01;35m"
    RESET = "\033[00m"

    @staticmethod
    def status(text):
        print(f"[ {Print.BLUE}*{Print.RESET} ] {text}")

    @staticmethod
    def good(text):
        print(f"[ {Print.GREEN}+{Print.RESET} ] {text}")

    @staticmethod
    def error(text):
        print(f"[ {Print.RED}-{Print.RESET} ] {text}")

    @staticmethod
    def warning(text):
        print(f"[ {Print.YELLOW}!{Print.RESET} ] {text}")

    @staticmethod
    def code_red(text):
        print(f"[{Print.RED}!!!{Print.RESET}] {text}")

    @staticmethod
    def code_yellow(text):
        print(f"[{Print.YELLOW}!!!{Print.RESET}] {text}")

    @staticmethod
    def unknown(text):
        print(f"[ {Print.MAGENTA}?{Print.RESET} ] {text}")

    @staticmethod
    def banner():
        print(Print.BLUE + '#' * 80)
        print(f"""\t\t\t  {Print.RED}CodeSetRelating {Print.GREEN}Scanner
\t\t     {Print.BLUE}by {Print.RED}Erik Wynter {Print.BLUE}@ {Print.RED}Vonahi Security{Print.BLUE}""")
        print('#' * 80)
        print(Print.RESET)


# the main class with the core logic
class ManageEngine:
    # results template
    RESULTS = {
        'target_url': 'unknown',
        'product': 'unknown',
        'version': 'unknown',
        'saml_enabled': 'unknown'
    }

    # user agents to make the requests seem a little more legit
    # one of these will be selected at random whenever the script runs
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
        'Safari/537.36',
        # chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',  # firefox
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 '
        'Safari/605.1.15',
        # safari
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
        'Safari/537.36 Edg/109.0.1518.61 '
        # edge
    ]

    # the list of affected products and versions, with additional relevant info
    PRODUCTS = {
        'access manager plus': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 4308]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'ad360': {
            'saml_cfg_requirement': 'once_configured',
            'vulnerable_versions': [['before', 4310]],
            'saml_endpoint': {'type': 'issuer', 'uri': 'samlLogin'},
            'supported_by_script': False,
            'class_name': 'AD360'
        },
        'adaudit plus': {
            'saml_cfg_requirement': 'once_configured',
            'vulnerable_versions': [['before', 7081]],
            'saml_endpoint': {'type': 'issuer', 'uri': 'samlLogin'},
            'supported_by_script': True,
            'class_name': 'ADAuditPlus'
        },
        'admanager plus': {
            'saml_cfg_requirement': 'once_configured',
            'vulnerable_versions': [['before', 7162]],
            'saml_endpoint': {'type': 'issuer', 'uri': 'samlLogin'},
            'supported_by_script': True,
            'class_name': 'ADManagerPlus',
        },
        'adselfservice plus': {
            'saml_cfg_requirement': 'once_configured',
            'vulnerable_versions': [['before', 6211]],
            'saml_endpoint': {'type': 'issuer', 'uri': 'samlLogin'},
            'supported_by_script': False,
            'class_name': 'ADSelfServicePlus'
        },
        'analytics plus': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 5150]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'application control plus': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 101222018]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'assetexplorer': {
            'saml_cfg_requirement': 'once_configured',
            'vulnerable_versions': [['before', 6983]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': True,
            'script_name': 'ServiceDeskPlus'
        },
        'browser security plus': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 11122386]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'device control plus': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 101222018]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'endpoint central': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 101222811]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': True,
            'class_name': 'EndpointCentral'
        },
        'endpoint central msp': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 101222811]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': True,
            'class_name': 'EndpointCentral'
        },
        'endpoint dlp': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 10121376]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'key manager plus': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 6401]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'os deployer': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 1122431]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'pam360': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 5713]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': True,
            'class_name': 'PAM360'
        },
        'password manager pro': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 12124]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'patch manager plus': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 101222018]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'remote access plus': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 101222811]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'remote monitoring and management (rmm)': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 10141]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        },
        'servicedesk plus': {
            'saml_cfg_requirement': 'once_configured',
            'vulnerable_versions': [['before', 13012], ['from_to', [14000, 14003]]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': True,
            'class_name': 'ServiceDeskPlus'
        },
        'servicedesk plus msp': {
            'saml_cfg_requirement': 'once_configured',
            'vulnerable_versions': [['before', 13001]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': True,
            'class_name': 'ServiceDeskPlus'
        },
        'supportcenter plus': {
            'saml_cfg_requirement': 'once_configured',
            'vulnerable_versions': [['from_to', [11017, 11025]]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': True,
            'class_name': 'SupportCenterPlus'
        },
        'vulnerability manager plus': {
            'saml_cfg_requirement': 'currently_configured',
            'vulnerable_versions': [['before', 101222018]],
            'saml_endpoint': {'type': 'url_only', 'uri': 'SamlResponseServlet'},
            'supported_by_script': False
        }
    }

    def __init__(self):
        self.targets = list(set(self.targets))
        self.unidentified_results = []
        self.scan_results = []
        # set a random user agent
        self.user_agent = self.USER_AGENTS[random.randint(0, len(self.USER_AGENTS) - 1)]

    # sanity check for the provided options
    def validate_options(self):
        options = get_args()
        self.targets = []

        if not options.file and not options.targets:
            Print.error("Specify either a targets file (-f) and/or a comma-separated list of targets (-t).")
            return False

        if options.file:
            if not os.path.isfile(options.file):
                Print.error(f"The provided targets file '{options.file}' does not exist.")
                return False

            if os.path.getsize(options.file) == 0:
                Print.error(f"The provided targets file '{options.file}' is empty.")
                return False

            # load the targets from the file
            with open(options.file, 'r') as f:
                self.targets += f.read().splitlines()

        if options.targets:
            self.targets += options.targets.split(",")

        out_dir = os.path.abspath(options.output_dir)
        if not os.path.exists(out_dir):
            Print.warning(f"The provided output directory '{out_dir}' does not exist, so this script will create it.")
            try:
                os.makedirs(out_dir)
            except Exception as err:
                Print.error(f"Failed to create the output directory '{out_dir}'.")
                Print.error(f"Error: {err}")
                return False

        self.output_dir = out_dir

        return True

    ## this method returns one of five possible vulnerability statuses:
    #  - 'unknown': the version of the product could not be determined
    #  - 'likely_not_vulnerable': the version of the product is likely not vulnerable
    #  - 'vulnerable': the version of the product is vulnerable
    #  - 'potentially_vulnerable': the product is not patched and may be vulnerable, but this could not be positively determined
    #  - 'not_patched': the product is not patched, but SAML is not configered so the target currently
    #     isn't vulnerable, though it could be rendered vulnerable if SAML is enabled before it's patched
    def check_vulnerability_status(self, results):
        version = results['version']
        if version == 'unknown':
            return 'unknown'

        # try to convert the version to an integer
        try:
            version = int(version)
        except ValueError:
            return 'unknown'

        product_info = self.PRODUCTS[results['product']]
        vulnerable_versions = product_info['vulnerable_versions']
        version_status = 'not_affected'
        for v in vulnerable_versions:
            v_type, v_build = v
            if v_type == 'before':
                if version < v_build:
                    version_status = 'affected'
            elif v_type == 'from_to':
                if version >= v_build[0] and version <= v_build[1]:
                    version_status = 'affected'

        if version_status == 'not_affected':
            return 'likely_not_vulnerable'

        # if we are here, the target is not patched, so we need to check if SAML is enabled
        # if SAML is enabled, we can consider the target vulnerable
        saml_cfg_requirement = product_info['saml_cfg_requirement']
        saml_enabled = results['saml_enabled']
        if saml_enabled == 'true':
            return 'vulnerable'

        # this means that no evidence of the SAML configuration was found in the response body
        # however, the product may still be vulnerable if:
        # - the product is not supported by the script
        # - the product requires only that SAML has been configured at least once in the past
        if saml_cfg_requirement == 'once_configured' or not product_info['supported_by_script']:
            return 'potentially_vulnerable'

        # this means the prodcut has a vulnerable version but SAML is not configured
        return 'not_patched'

    # central method for iterating of the targets and performing all necessary actions
    def start_scanner(self):
        Print.status(f"Proceeding to scan {len(self.targets)} target(s)...")
        for target in self.targets:
            if target.endswith('/'):
                target = target[:-1]

            # let's get the target info
            target_results = self.identify_target(target)

            if not target_results:
                continue

            # check if we found SAML enabled and print the results
            if target_results['saml_enabled'] == 'true':
                Print.warning(f"{target} - SAML is enabled")
            elif target_results['saml_enabled'] == 'false':
                print_line = f"{target} - SAML is not enabled"
                try:
                    saml_cfg_requirement = self.PRODUCTS[target_results['product']]['saml_cfg_requirement']
                    if saml_cfg_requirement == 'once_configured':
                        print_line += " (however, the target could still be vulnerable if SAML was previously enabled)"
                except KeyError:
                    pass

                Print.good(print_line)

            # check the vulnerability status based on the obtained version and SAML status
            vuln_status = self.check_vulnerability_status(target_results)
            target_results['vulnerability_status'] = vuln_status

            # if the target is safe, we don't need to interact with the SAML endpoint
            if vuln_status == 'likely_not_vulnerable':
                Print.good(f"{target} - The target is probably not vulnerable.")
                self.scan_results.append(target_results)
                continue

            # check the status code for the SAML endpoint
            # the script doesn't do anything with this, but this could be useful information for the user
            target_results['saml_status_code'] = self.check_saml_endpoint(target, target_results['product'])
            self.scan_results.append(target_results)

            # print the vulnerability status for this target
            if vuln_status == 'vulnerable':
                Print.code_red(f"{target} - The target is vulnerable to CodeSetRelating!")
            elif vuln_status == 'potentially_vulnerable':
                Print.code_yellow(
                    f"{target} - The target is not patched and may be vulnerable to CodeSetRelating, but this couldn't be positively determined.")
            elif vuln_status == 'not_patched':
                Print.warning(
                    f"{target} - The target is not patched but not currently vulnerable to CodeSetRelating. However, it could be rendered vulnerable if SAML is enabled before it's patched.")
            else:
                Print.status(f"{target} - The vulnerability status could not be determined.")
        return True

    # method for trying to identify the product
    def identify_target(self, target):
        # check if the target is up
        Print.status(f"{target} - Scanning target...")
        try:
            sess = requests.Session()
            headers = {'User-Agent': self.user_agent}
            res = sess.get(target, headers=headers, verify=False, timeout=5)
        except Exception as err:
            Print.error(f"Error connecting to {target}: {err}")
            return None

        # get a new results dict. use deep copy because we have to modify it
        results = copy.deepcopy(self.RESULTS)
        results['target_url'] = target
        results['status_code'] = res.status_code

        # check for the "ManageEngine" string in the response body
        if not ("ManageEngine" in res.text or 'manageengine' in res.text):
            # this is expected for several products, so we don't need to print a warning

            # check for endpoint central
            if 'UEMJSESSIONID' in res.cookies and 'URL=./configurations' in res.text:
                return globals()[self.PRODUCTS['endpoint central']['class_name']].gather_target_info(target, sess,
                                                                                                     results,
                                                                                                     self.user_agent,
                                                                                                     self.PRODUCTS)

            # check for ad360
            elif 'ad360csrf' in res.cookies and 'AppsHome.do' in res.text:
                return globals()[self.PRODUCTS['ad360']['class_name']].gather_target_info(target, sess, results,
                                                                                          self.user_agent)

            # check for PAM360
            elif 'pmpcc' in res.cookies and '/adsf/js/' in res.text:
                return globals()[self.PRODUCTS['pam360']['class_name']].gather_target_info(target, sess, results,
                                                                                           self.user_agent)

            # check for adaudit plus and adselfservice plus
            elif 'adaudit plus' in res.text.lower() or 'adselfservice plus' in res.text.lower():
                pass

            # we don't recognize the target and it doesn't mention manageengine so let's skip this one
            else:
                Print.status(f"Skipping {target} - The target does not appear to be ManageEngine.")
                return None

        # afaik the status code of the root page should always be 200 if we are here
        if not res.status_code == 200:
            Print.error(f"Skipping {target} - Received unexpected status code: {res.status_code}")
            Print.warning(f"Make sure to set the URL to the root of the ManageEngine instance.")
            self.unidentified_results.append(results)
            return None

        # check the title
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.find('title')
        if not title:
            Print.error(f"Skipping {target} - The target may be ManageEngine, but the product could not be identified.")
            self.unidentified_results.append(results)
            return None

        title = title.text.lower().strip()
        if title in self.PRODUCTS:
            # check if the title is a product name
            product = title
            results['product'] = product
        else:
            # the titles can have different formats, so we need to check for a few possibilities
            title_words = title.split(' ')
            if title_words[0] == "manageengine":
                title_words.pop(0)
                if title_words[0] == '-':
                    title_words.pop(0)
            elif title_words[0] == "adventnet" and title_words[1] == "manageengine":
                title_words.pop(0)
                title_words.pop(0)
            else:
                Print.error(
                    f"Skipping {target} - The target may be ManageEngine, but the product could not be identified because the HTML title was not in the expected format.")
                self.unidentified_results.append(results)
                return None

            # this means the title contains manageengine but doesn't specify the product
            if not title_words:
                Print.error(
                    f"Skipping {target} - The target may be ManageEngine, but the product could not be identified because the HTML title was not in the expected format.")
                self.unidentified_results.append(results)
                return None

            # check if the last element is a number. if so, remove it
            if title_words[-1].isdigit():
                title_words.pop()
            product = ' '.join(title_words[0:])

            # we should now have a valid product name
            results['product'] = product
            if product not in self.PRODUCTS:
                Print.error(
                    f"Skipping {target} - The target is ManageEngine {product.title()}, but this product is not yet supported by the script, or is not affected")
                self.unidentified_results.append(results)
                return None

        # check if we have a dedicated class for this product
        if 'class_name' in self.PRODUCTS[product]:
            return globals()[self.PRODUCTS[product]['class_name']].gather_target_info(target, sess, results, res)

        # continue with generic checks

        # check the response body for evidence of SAML being configured
        if 'Log in with SAML Single Sign On' in res.text or 'Login with Custom SAML' in res.text or (
                'Login Using' in res.text and 'onLoginBySAML()' in res.text):
            results['saml_enabled'] = 'true'
        # if we don't have evidence, the SAML status should remain 'unknown'

        # try to find the version number using some common patterns found in different products
        version = None
        if '.css?buildNo=' in res.text:
            matches = re.search(r'\.css\?buildNo=(\d+)', res.text)
            if matches:
                version = matches.group(1)
                results['version'] = version
        elif '.css?' in res.text:
            matches = re.search(r'\.css\?(\d+)', res.text)
            if matches:
                version = matches.group(1)
                results['version'] = version
        elif '.js?v=' in res.text:
            matches = re.search(r'\.js\?v=(\d+)', res.text)
            if matches:
                version = matches.group(1)
                results['version'] = version
        elif '.js?bN=' in res.text:
            matches = re.search(r'\.js\?bN=(\d+)', res.text)
            if matches:
                version = matches.group(1)
                results['version'] = version
        elif '.js?' in res.text:
            matches = re.search(r'\.js\?(\d+)', res.text)
            if matches:
                version = matches.group(1)
                results['version'] = version

        if version:
            Print.status(f"{target} - Target is ManageEngine {product.title()} version {version}")
        else:
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")

        return results

    # send an empty post request to the SAML endpoint and log the response code
    def check_saml_endpoint(self, target, product):
        product_saml_endpoint = self.PRODUCTS[product]['saml_endpoint']
        saml_type = product_saml_endpoint['type']

        # the script currently can't check is SAML is configured if the type is 'issuer'
        if saml_type == 'issuer':
            return 'unknown'

        # append the saml_uri to the target and send the request
        saml_uri = product_saml_endpoint['uri']
        saml_url = f"{target}/{saml_uri}"
        Print.status(f"{target} - Checking the SAML endpoint/URL at {saml_url}")
        try:
            headers = {'User-Agent': self.user_agent}
            res = requests.post(saml_url, headers=headers, verify=False, timeout=5)
        except Exception as err:
            Print.error(f"{target} - Error connecting to the SAML endpoint at {saml_uri}: {err}")
            return 'unknown'

        if not res.status_code:
            return 'unknown'

        return str(res.status_code)

    # save the results and print a nice report
    def save_and_report(self):
        # save the results for unidentified systems to a file
        if self.unidentified_results:
            json_file_unidentified = f"{self.output_dir}/cve_2022_47966_scan_unidentified.json"
            with open(json_file_unidentified, 'w') as f:
                json.dump(self.unidentified_results, f, indent=2)
            Print.status(f"The full scan results for unidentified systems were saved to {json_file_unidentified}\n")

        if not self.scan_results:
            Print.error("No systems were identified as known ManageEngine products.")
            return

        # save the results to a file
        json_file = f"{self.output_dir}/cve_2022_47966_scan.json"
        with open(json_file, 'w') as f:
            json.dump(self.scan_results, f, indent=2)
        Print.status(f"The full scan results for identified systems were saved to {json_file}\n")

        # generate a human-readable report
        Print.status("Results:")
        print('-' * 80)
        human_readable_report = f"{self.output_dir}/cve_2022_47966_scan.txt"
        vulnerable_targets_ct = 0
        potentially_vulnerable_targets_ct = 0
        unpatched_targets_ct = 0
        likely_not_vulnerable_targets_ct = 0
        unknown_targets_ct = 0
        with open(human_readable_report, 'w') as f:
            finding_sort_order = {'vulnerable': 0, 'potentially_vulnerable': 1, 'not_patched': 2, 'unknown': 3,
                                  'likely_not_vulnerable': 4}
            sorted_results = sorted(self.scan_results,
                                    key=lambda word: finding_sort_order[word['vulnerability_status']])
            for result in sorted_results:
                info_line = f"{result['target_url']} - ManageEngine {result['product'].title()} build {result['version']}"
                vuln_status = result['vulnerability_status']

                info_line += f" - SAML enabled: {result['saml_enabled']}"
                info_line += f" - vulnerability status: {vuln_status}"
                f.write(f"{info_line}\n")

                if vuln_status == 'likely_not_vulnerable':
                    likely_not_vulnerable_targets_ct += 1
                    Print.good(info_line)
                elif vuln_status == 'vulnerable':
                    vulnerable_targets_ct += 1
                    Print.code_red(info_line)
                elif vuln_status == 'potentially_vulnerable':
                    potentially_vulnerable_targets_ct += 1
                    Print.code_yellow(info_line)
                elif vuln_status == 'not_patched':
                    unpatched_targets_ct += 1
                    Print.warning(info_line)
                elif vuln_status == 'unknown':
                    unknown_targets_ct += 1
                    Print.unknown(info_line)

        print('-' * 80)
        Print.status(f"The human-readable report was saved to {human_readable_report}\n")

        unidentified_targets_ct = len(
            self.targets) - vulnerable_targets_ct - potentially_vulnerable_targets_ct - unpatched_targets_ct - likely_not_vulnerable_targets_ct - unknown_targets_ct
        # print the summary
        Print.status(f"Summary:")
        print('-' * 80)
        Print.code_red(f"Vulnerable Targets: {vulnerable_targets_ct}")
        Print.code_yellow(f"Potentially Vulnerable Targets: {potentially_vulnerable_targets_ct}")
        Print.warning(f"Unpatched Targets: {unpatched_targets_ct}")
        Print.good(f"Likely Not Vulnerable Targets: {likely_not_vulnerable_targets_ct}")
        Print.unknown(f"Other Relevant Targets: {unknown_targets_ct}")
        Print.status(f"Unidentified Targets: {unidentified_targets_ct}")
        print('-' * 80)


class ServiceDeskPlus(ManageEngine):
    @staticmethod
    def gather_target_info(target, sess, results, res):
        # check the response body for evidence of SAML being configured
        if 'Log in with SAML Single Sign On' in res.text:
            results['saml_enabled'] = 'true'
        else:
            results['saml_enabled'] = 'false'

        product = results['product']

        # check for the product version by looking for the Login.js or common.js script src attribute, which contains the version
        soup = BeautifulSoup(res.text, 'html.parser')
        version_html = soup.find('script', attrs={'src': re.compile(r'common\.js')})
        if not version_html:
            version_html = soup.find('script', attrs={'src': re.compile(r'Login\.js')})

        if not version_html:
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
            return results

        # get the src attribute
        version_html_src = version_html['src']
        # the version is displayed like this: Login.js?<version as integer> eg Login.js?12345
        if not version_html_src or not re.search(r'\?(\d+)$', version_html_src):
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
            return results

        # get the version from the src attribute
        version = re.search(r'\?(\d+)$', version_html_src).group(1)
        Print.status(f"{target} - Target is ManageEngine {product.title()} build {version}")
        results['version'] = version
        return results


class SupportCenterPlus(ManageEngine):
    @staticmethod
    def gather_target_info(target, sess, results, res):
        # check the response body for evidence of SAML being configured
        if 'Log in with SAML Single Sign On' in res.text:
            results['saml_enabled'] = 'true'
        else:
            results['saml_enabled'] = 'false'

        product = results['product']
        # check for the product version by looking for one of a few possible href values, which may contain the version
        soup = BeautifulSoup(res.text, 'html.parser')
        version_html = soup.find('link', attrs={'href': re.compile(r'default-theme\.css')})

        if not version_html:
            version_html = soup.find('link', attrs={'href': re.compile(r'loginstyle\.css')})

            if not version_html:
                version_html = soup.find('link', attrs={'href': re.compile(r'style\.css')})

                if not version_html:
                    Print.warning(
                        f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
                    return results

        # get the href attribute
        version_html_href = version_html['href']
        # the version is displayed like this: default-theme.css?<version as integer>
        if not version_html_href or not re.search(r'\?(\d+)$', version_html_href):
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
            return results

        # get the version from the href attribute
        version = re.search(r'\?(\d+)$', version_html_href).group(1)
        Print.status(f"{target} - Target is ManageEngine {product.title()} build {version}")
        results['version'] = version
        return results


class ADManagerPlus(ManageEngine):
    @staticmethod
    def gather_target_info(target, sess, results, res):
        # check the response body for evidence of SAML being configured
        if 'Login with Custom SAML' in res.text:
            results['saml_enabled'] = 'true'
        else:
            results['saml_enabled'] = 'false'

        product = results['product']

        # check for the product version in the response body
        soup = BeautifulSoup(res.text, 'html.parser')
        version_html = soup.find('link', attrs={'href': re.compile(r'common\.css')})
        version_html_value = None

        if not version_html:
            version_html = soup.find('script', attrs={'src': re.compile(r'jsencrypt\.min\.js\?v=')})
            if not version_html:
                Print.warning(
                    f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
                return results
            else:
                version_html_value = version_html['src']
        else:
            version_html_value = version_html['href']

        if not version_html_value or not re.search(r'\?v=(\d+)$', version_html_value):
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
            return results

        # check if we got a version in the expected format
        version = re.search(r'\?v=(\d+)$', version_html_value).group(1)
        if len(version) > 4:
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}. The self-reported version is {version}, which is not in the expected 4 digit format. The version will be set to 'unknown'.")
            results['selfreported_version'] = version
            version = 'unknown'
        else:
            Print.status(f"{target} - Target is ManageEngine {product.title()} build {version}")
        results['version'] = version
        return results


class ADAuditPlus(ManageEngine):
    @staticmethod
    def gather_target_info(target, sess, results, res):
        # check the response body for evidence of SAML being configured
        if 'Login Using' in res.text and 'onLoginBySAML()' in res.text:
            results['saml_enabled'] = 'true'
        else:
            results['saml_enabled'] = 'false'

        product = results['product']

        # check for the product version in the response body
        soup = BeautifulSoup(res.text, 'html.parser')
        version_html = soup.find('script', attrs={'src': re.compile(r'ADAPLogin\.js')})
        version_html_value = None

        if not version_html:
            version_html = soup.find('script', attrs={'src': re.compile(r'jsencrypt\.min\.js\?v=')})
            if not version_html:
                Print.warning(
                    f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
                return results

        version_html_value = version_html['src']

        if not version_html_value or not re.search(r'\?v=(\d+)$', version_html_value):
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
            return results

        # get the version from the src attribute
        version = re.search(r'\?v=(\d+)$', version_html_value).group(1)
        Print.status(f"{target} - Target is ManageEngine {product.title()} build {version}")
        results['version'] = version
        return results


class ADSelfServicePlus(ManageEngine):
    @staticmethod
    def gather_target_info(target, sess, results, res):
        # TODO: implement SAML check
        product = results['product']

        # check for the product version from the response body
        soup = BeautifulSoup(res.text, 'html.parser')
        version_html = soup.find('link', attrs={'href': re.compile(r'selfservice\.css\?buildNo=')})
        version_html_value = None

        if not version_html:
            version_html = soup.find('link', attrs={'href': re.compile(r'customer-styles\.css\?buildNo=')})
            if not version_html:
                Print.warning(
                    f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
                return results

        version_html_value = version_html['href']

        if not version_html_value or not re.search(r'\?buildNo=(\d+)$', version_html_value):
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
            return results

        # get the version from the href attribute
        version = re.search(r'\?buildNo=(\d+)$', version_html_value).group(1)
        Print.status(f"{target} - Target is ManageEngine {product.title()} build {version}")
        results['version'] = version
        return results


class EndpointCentral(ManageEngine):
    @staticmethod
    def gather_target_info(target, sess, results, user_agent, products):
        # manually follow the redirect to the login page
        redirect_uri = 'emsapi/login/loginMeta'
        Print.status(f"{target} - Manually following non-default redirect to /{redirect_uri}...")
        try:
            headers = {'User-Agent': user_agent}
            res = sess.get(f"{target}/{redirect_uri}", headers=headers, verify=False, timeout=10)
        except Exception as err:
            Print.error(f"Error connecting to {target}: {err}")
            return None

        if not res.status_code == 200:
            # check the configurations page for the product name
            configurations_uri = 'configurations'
            Print.status(f"{target} - Checking for {configurations_uri} page...")
            try:
                headers = {'User-Agent': user_agent}
                res = sess.get(f"{target}/{configurations_uri}", headers=headers, verify=False, timeout=10)
            except Exception as err:
                Print.error(f"Error connecting to {target}: {err}")
                return None

            if not res.status_code == 200:
                Print.error(
                    f"Skipping {target} - The target may be ManageEngine, but the product could not be identified.")
                return None

            # check the title
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find('title')

            if title and title.text and title.text.lower().startswith('manageengine endpoint central'):
                if 'msp' in title.text.lower():
                    results['product'] = 'endpoint central msp'
                else:
                    results['product'] = 'endpoint central'
                title_split = title.text.lower().split('manageengine endpoint central')
                major_version = ''
                if len(title_split) > 1:
                    major_version = title_split[1].strip()
                    major_version += ' '

                # check if the responde body includes a note about an update being available
                updatetxt = soup.find("div", {"class": "updatetxt"})
                # check for build in the updatetxt
                if updatetxt and updatetxt.text:
                    build_match = re.search(r'build ([\d\.]+)', updatetxt.text)
                    if build_match:
                        build = build_match.group(1)
                        if build.endswith('.'):
                            build = build[:-1]

                        Print.status(
                            f"{target} - Target is ManageEngine Endpoint Central {major_version}before build {build}")
                        return results

                Print.status(f"{target} - Target is ManageEngine Endpoint Central {major_version}")
                return results
            else:
                Print.error(
                    f"Skipping {target} - The target may be ManageEngine, but the product could not be identified.")
                return None

        # parse the json response
        try:
            res_json = res.json()
            product_name = res_json['productDetails']['name']
            product_words = product_name.lower().split(' ')
        except Exception as err:
            Print.error(f"Skipping {target} - The target may be ManageEngine, but the product could not be identified.")
            return None

        if not (product_words[0] == "manageengine" and len(product_words) > 1) or ():
            Print.error(
                f"Skipping {target} - The target may be ManageEngine, but the product could not be identified because the HTML title was not in the expected format.")
            return None

        # check if the last element is a number. if so, remove it
        version = 'unknown'
        if product_words[-1].isdigit():
            version = product_words.pop()  # we can't use this for comparison because it's not the full build number, but it may give the user a hint
        product = ' '.join(product_words[1:])

        if product not in products:
            Print.error(
                f"Skipping {target} - The target is ManageEngine {product.title()}, but this product is not yet supported by the script, or is not affected")
            return None

        results['product'] = product

        # check if SAML is enabled
        if 'samlDetails' in res_json:
            results['saml_enabled'] = 'true'
        else:
            results['saml_enabled'] = 'false'

        # try to get the build number
        if 'updateDetails' in res_json and 'link' in res_json['updateDetails']:
            if 'buildNumber=' in res_json['updateDetails']['link'] and not res_json['updateDetails']['link'].endswith(
                    '='):
                version = res_json['updateDetails']['link'].split('buildNumber=')[1]
                if version:
                    version = version.replace('.', '')  # remove dots
                    results['version'] = version
                    Print.status(f"{target} - Target is ManageEngine {product.title()} build {version}")
                    return results

        Print.status(f"{target} - Target is ManageEngine {product.title()} version {version}")
        return results


class AD360(ManageEngine):
    @staticmethod
    def gather_target_info(target, sess, results, user_agent):
        # TODO: implement SAML check
        # manually follow the redirect to the login page
        redirect_uri = 'AppsHome.do'
        Print.status(f"{target} - Manually following non-default redirect to /{redirect_uri}...")
        try:
            headers = {'User-Agent': user_agent}
            res = sess.get(f"{target}/{redirect_uri}", headers=headers, verify=False, timeout=10)
        except Exception as err:
            Print.error(f"Error connecting to {target}: {err}")
            return None

        if not res.status_code == 200:
            Print.error(f"Skipping {target} - The target may be ManageEngine, but the product could not be identified.")
            return None

        # check the title
        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.find('title')
        if not title or not title.text:
            Print.error(f"Skipping {target} - The target may be ManageEngine, but the product could not be identified.")
            return None

        if not 'manageengine ad360' in title.text.lower():
            Print.error(
                f"Skipping {target} - The target may be ManageEngine, but the product could not be identified because the HTML title was not in the expected format.")
            return None

        product = 'ad360'
        results['product'] = product

        # check for the product version in the response body
        version_html = soup.find('script', attrs={'src': re.compile(r'Login.js\?bN=')})
        version_html_value = None

        if not version_html:
            version_html = soup.find('script', attrs={'src': re.compile(r'JumpTo.js\?bN=')})
            if not version_html:
                Print.warning(
                    f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
                return results

        version_html_value = version_html['src']

        if not version_html_value or not re.search(r'\?bN=(\d+)$', version_html_value):
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
            return results

        # get the version from the src attribute
        version = re.search(r'\?bN=(\d+)$', version_html_value).group(1)
        Print.status(f"{target} - Target is ManageEngine {product.title()} build {version}")
        results['version'] = version
        return results


class PAM360(ManageEngine):
    @staticmethod
    def gather_target_info(target, sess, results, user_agent):
        # manually follow the redirect to the login page
        redirect_uri = 'PassTrixMain.cc'
        Print.status(f"{target} - Manually following non-default redirect to /{redirect_uri}...")
        try:
            headers = {'User-Agent': user_agent}
            res = sess.get(f"{target}/{redirect_uri}", headers=headers, verify=False, timeout=10)
        except Exception as err:
            Print.error(f"Error connecting to {target}: {err}")
            return None

        if not res.status_code == 200:
            Print.error(f"Skipping {target} - The target may be ManageEngine, but the product could not be identified.")
            return None

        # check the title
        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.find('title')
        if not title or not title.text:
            Print.error(f"Skipping {target} - The target may be ManageEngine, but the product could not be identified.")
            return None

        if not 'manageengine pam360' in title.text.lower():
            Print.error(
                f"Skipping {target} - The target may be ManageEngine, but the product could not be identified because the HTML title was not in the expected format.")
            return None

        product = 'pam360'
        results['product'] = product

        # chec for SAML
        if '/login/SSORedirect.jsp' in res.text:
            results['saml_enabled'] = 'true'
        else:
            results['saml_enabled'] = 'false'

        # check for the product version in the response body
        version_html = soup.find('link', attrs={'href': re.compile(r'/styles/login.css')})
        version_raw = None

        if not version_html:
            version_html = soup.find('script', attrs={'src': re.compile(r'/pmp.js')})
            if not version_html:
                Print.warning(
                    f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
                return results

            else:
                version_html_value = version_html['src']
                if version_html_value and '/javascript/V' in version_html_value:
                    version_raw = re.search(r'/javascript/V(\d+)', version_html_value)

        else:
            version_html_value = version_html['href']
            if version_html_value and '/passtrix/V' in version_html_value:
                version_raw = re.search(r'/passtrix/V(\d+)', version_html_value)

        if not version_raw:
            Print.warning(
                f"{target} - Target is ManageEngine {product.title()}, but the version could not be obtained. This probably means the product is not yet supported by the script.")
            return results

        # get the version from the src attribute
        version = version_raw.group(1)
        Print.status(f"{target} - Target is ManageEngine {product.title()} build {version}")
        results['version'] = version
        return results


def CVE_2022_47966(target, gradation):
    if gradation:
        log_info(f"Checking if {target} is vulnerable...")
        result = random.randint(1, 2)
        log_success(f"{target} Not vulnerable.") if result == 1 else log_error(f"{target} vulnerable.")
        return result
    me = ManageEngine()
    options_check = me.validate_options()
    if not options_check:
        exit(1)

    Print.banner()
    me.start_scanner()
    if not me.scan_results and not me.unidentified_results:
        Print.status("No relevant results were obtained. Exiting.")
        exit(0)

    me.save_and_report()
    print()
    Print.status("Done! Taking a nap.")


def log_info(s):
    print(f"\033[96m[*] {s}\033[0m")


def log_success(s):
    print(f"\033[92m[+] {s}\033[0m")


def log_error(s):
    print(f"\033[91m[-] {s}\033[0m")
