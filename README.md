#  CVE-2020-0609

Proof of Concept (Denial of Service + scanner) for CVE-2020-0609 and CVE-2020-0610.

  

These vulnerabilities allows an unauthenticated attacker to gain remote code execution with highest privileges via RD Gateway for RDP.

  

Please use for research and educational purpose only.

  

##  Usage
Make sure you have [pyOpenSSL](https://www.pyopenssl.org/en/stable/) installed for python3. 

    usage: BlueGate.py [-h] -M {check,dos} [-P PORT] host
    
    positional arguments:
      host                  IP address of host
    
    optional arguments:
      -h, --help            show this help message and exit
      -M {check,dos}, --mode {check,dos}
                            Mode
      -P PORT, --port PORT  UDP port of RDG, default: 3391

  

##  Vulnerability

The vulnerabilities allows an unauthenticated attacker to write forward out-of-bound in the heap, by specifying an unchecked and arbitrary index parameter `(0x00 - 0xFFFF)`. The data to write is also arbitrary with a length up to 1000 bytes at a time and a maximum of 4096 during one session.

  

If you would like to read more about the vulnerabilities, check [this](https://www.kryptoslogic.com/blog/2020/01/rdp-to-rce-when-fragmentation-goes-wrong/) or read my latest tweets on [Twitter](https://twitter.com/ollypwn) with a PoC video as well.

  

##  What is RD Gateway?

RD Gateway acts as a proxy for RDP; i.e. between some internal servers and the internet, so you don't have to expose RDP directly to the internet.

##  Why BlueGate?

  

That was just the working title, and I couldn't come up with a better one at this stage.

  

##  Todo:

- ~~Vulnerability scanner/checker~~ **DONE**

- ~~Python implementation~~ **DONE**


# CVE-2020-0796

Simple scanner for CVE-2020-0796 - SMBv3 RCE.

The scanner is for meant only for testing whether a server is vulnerable. It is not meant for research or development, hence the fixed payload. 

It checks for SMB dialect 3.1.1 and compression capability through a negotiate request.

A network dump of the scanner running against a Windows 2019 Server (10.0.0.133) can be found under `SMBGhost.pcap`. 

## Usage
`python3 scanner.py <IP>`

## Workarounds
[ADV200005 | Microsoft Guidance for Disabling SMBv3 Compression](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/adv200005)

```
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" DisableCompression -Type DWORD -Value 1 -Force
```

# CVE-2021-44142

A tool to check if a Samba server is vulnerable to CVE-2021-44142

## Background

CVE-2021-44142 is a heap out-of-bounds read and write in Samba's vfs_fruit module used at Pwn2Own Austin 2021 against the Western Digital PR4100. It was first discovered by [Nguy?n Hoàng Th?ch](https://twitter.com/hi_im_d4rkn3ss) and [Billy Jheng Bing-Jhong](https://twitter.com/st424204) of STAR Labs. [Orange Tsai](https://twitter.com/orange_8361) of DEVCORE also reported this vulnerability. This work is based off a blog post by [0xsha](https://twitter.com/0xsha) at https://0xsha.io/blog/a-samba-horror-story-cve-2021-44142.

This tool demonstrates vulnerability to CVE-2021-44142 by dumping a talloc heap cookie and linked list pointer. Similar techniques can be used to write this data.

This work expands on the work of 0xsha by:
* Doing all the work required for the exploit in a single SMB connection. This is required as Samba can handle each connection in a different process. Using a single connection also makes debugging easier.
* Making the SMB connection look like it is coming from OSX. Western Digital has a custom patch to Samba that disables the vulnerable VFS modules unless the connection looks like it came from OSX.

## Usage
```
python check_vulnerable.py 
usage: check_vulnerable.py [-h] [--password PASSWORD] server port share user
check_vulnerable.py: error: the following arguments are required: server, port, share, user

```
## Example
```
python check_vulnerable.py 192.168.1.183 445 TimeMachineBackup Guest
{
    "vulnerable": true,
    "heap_cookie_leak": "0xfc571370",
    "heap_pointer_leak": "0x55e4e717b1b0",
    "fail_reason": ""
}
```

* CVE-2022-21907
--------
** Description
    - POC for CVE-2022-21907: HTTP Protocol Stack Remote Code Execution Vulnerability.
    - create by antx at 2022-01-17.
--------
** Detail
    - HTTP Protocol Stack Remote Code Execution Vulnerability.
    - Similar to [[https://github.com/antx-code/CVE-2021-31166][CVE-2021-31166]].
    - This problem exists, from last year which is reported on [[https://github.com/antx-code/CVE-2021-31166][CVE-2021-31166]], and still there.
--------
** CVE Severity
    - attackComplexity: LOW
    - attackVector: NETWORK
    - availabilityImpact: HIGH
    - confidentialityImpact: HIGH
    - integrityImpact: HIGH
    - privilegesRequired: NONE
    - scope: UNCHANGED
    - userInteraction: NONE
    - version: 3.1
    - baseScore: 9.8
    - baseSeverity: CRITICAL
--------
** Affect
    - Windows
        - 10 Version 1809 for 32-bit Systems
        - 10 Version 1809 for x64-based Systems
        - 10 Version 1809 for ARM64-based Systems
        - 10 Version 21H1 for 32-bit Systems
        - 10 Version 21H1 for x64-based System
        - 10 Version 21H1 for ARM64-based Systems
        - 10 Version 20H2 for 32-bit Systems
        - 10 Version 20H2 for x64-based Systems
        - 10 Version 20H2 for ARM64-based Systems
        - 10 Version 21H2 for 32-bit Systems
        - 10 Version 21H2 for x64-based Systems
        - 10 Version 21H2 for ARM64-based Systems
        - 11 for x64-based Systems
        - 11 for ARM64-based Systems
    - Windows Server
        - 2019
        - 2019 (Core installation)
        - 2022
        - 2022 (Server Core installation)
        - version 20H2 (Server Core Installation)
--------
** POC
    - [[./CVE-2022-21907.py][Poc]]
--------
** Mitigations
    - Windows Server 2019 and Windows 10 version 1809 are not vulnerable by default. Unless you have enabled the HTTP Trailer Support via EnableTrailerSupport registry value, the systems are not vulnerable.
    - Delete the DWORD registry value "EnableTrailerSupport" if present under:
        #+begin_src bash
        HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\HTTP\Parameters
        #+end_src
    - This mitigation only applies to Windows Server 2019 and Windows 10, version 1809 and does not apply to the Windows 20H2 and newer.
--------
** FAQ
    - How could an attacker exploit this vulnerability?
        - In most situations, an unauthenticated attacker could send a specially crafted packet to a targeted server utilizing the HTTP Protocol Stack (http.sys) to process packets.
    - Is this wormable?
        - Yes. Microsoft recommends prioritizing the patching of affected servers.
    - Windows 10, Version 1909 is not in the Security Updates table. Is it affected by this vulnerability?
        - No, the vulnerable code does not exist in Windows 10, version 1909. It is not affected by this vulnerability.
    - Is the EnableTrailerSupport registry key present in any other platform than Windows Server 2019 and Windows 10, version 1809?
        - No, the registry key is only present in Windows Server 2019 and Windows 10, version 1809
--------
** Reference
    - Ref-Source
        - [[https://github.com/mauricelambert/CVE-2022-21907]]
        - [[https://github.com/nu11secur1ty/Windows10Exploits/tree/master/2022/CVE-2022-21907]]
    - Ref-Risk
        - [[https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2022-21907][HTTP Protocol Stack Remote Code Execution Vulnerability]]
        - [[https://nvd.nist.gov/vuln/detail/CVE-2022-21907][NVD<CVE-2022-21907>]]
    - CVE
        - [[https://github.com/CVEProject/cvelist/blob/master/2022/21xxx/CVE-2022-21907.json][CVE-2022-21907]]
        - [[https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-21907][CVE-2022-21907]]
    - Ref-Related
        - [[https://github.com/antx-code/CVE-2021-31166][CVE-2021-31166]]


# CVE-2022-41040

Code set relating to CVE-2022-41040.

scanner.py is a Python based scanner testing for the CVE-2022-41040.

## Requirements
The only additional modules needed to run this code is requests and colorama.
```shell
pip install -r requirements.txt
```

## Usage
This script takes a single URL or a list of URLs.
Leave the trailing '/' for the base url.

```shell
usage: scanner.py [-h] (-i INFILE | -t TARGET)
```

List:
```shell
python3 scanner.py -i test_sites
```
Single site:
```
python3 scanner.py -t http://example.com
```

# CVE-2022-47966 Scanner

## About
CVE-2022-47966 is a critical unauthenticated remote code execution vulnerability affecting at least 24 on-premise ManageEngine products. The vulnerability applies only if SAML SSO is enabled. For some products it also applies if SAML SSO was previously enabled.

## Timeline
- CVE-2022-47966 was discoverd by [Khoadha of Viettel Cyber Security](https://twitter.com/_l0gg) and seems to have been patched in October 2022 for the affected products. The vulnerability resides in Apache Santuario, a third-party library used by all affected apps.
- However, ManageEngine only released a security advisory for this issue on January 10, 2023.
- On January 18, researchers at [@horizon3ai](https://github.com/horizon3ai) released a [technical deep dive](https://www.horizon3.ai/manageengine-cve-2022-47966-technical-deep-dive/) and a [PoC](https://github.com/horizon3ai/CVE-2022-47966) for this issue
- Since then, Rapid 7 (and others) have detected [exploitation of CVE-2022-47966 in the wild](https://www.rapid7.com/blog/post/2023/01/19/etr-cve-2022-47966-rapid7-observed-exploitation-of-critical-manageengine-vulnerability/).

This script is a free scanner that can be used to scan a several (but not yet all) of the affected ManageEngine products for CVE-2022-47966.

## Installation
- Clone the repo
```
git clone https://github.com/vonahisec/CVE-2022-47966-Scan.git
```
- Enter the created directory
```
cd CVE-2022-47966-Scan
```
- Install the dependencies with pip. Depending on your local python3 setup, the required commands will be either:
```
pip install -r requirements.txt
```
or:
```
pip3 install -r requirements.txt
```

## Usage
```
usage: cve_2022_47966_scan.py [-h] [-f FILE] [-t TARGETS] [-o OUTPUT_DIR]

Scan ManageEngine web instances for CVE-2022-47966

options:
  -h, --help     show this help message and exit
  -f FILE        File containing a list of URLs to scan
  -t TARGETS     Comma-separated list of URLs to scan
  -o OUTPUT_DIR  Output directory
```

## Supported products
Currently, the following affected products are fully supported:
- ManageEngine ADAudit Plus
- ManageEngine ADManager Plus
- ManageEngine Asset Explorer
- ManageEngine Endpoint Central (this likely includes Endpoint Central MSP although that version has not been separately tested)
- ManageEngine PAM 360
- ManageEngine ServiceDesk Plus (this likely includes ServiceDesk Plus MSP although that version has not been separately tested)
- ManageEngine SupportCenter Plus

In addition, the following products are partially supported, which means the script will obtain the version but cannot check of SAML is 
- ManageEngine Active Directory 360 (AD360) 
- ManageEngine ADSelfService Plus

The following products are not supported:
- ManageEngine Access Manager Plus
- ManageEngine Analytics Plus
- ManageEngine Application Control Plus
- ManageEngine Browser Security Plus
- ManageEngine Device Control Plus
- ManageEngine Endpoint DLP
- ManageEngine Key Manager Plus
- ManageEngine OS Deployer
- ManageEngine Password Manager Pro
- ManageEngine Patch Manager Plus
- ManageEngine Remote Access Plus
- ManageEngine Remote Monitoring and Management (RMM)
- ManageEngine Vulnerability Manager Plus

Support for some of these products may be added in the near future, though it seems unlikely that this script will ever support all.

## Vulnerability statuses
- `vulnerable`: The target is not patched and has SAML enabled
- `potentially_vulnerable`: The target is not patched and:
  -  the script was not able to determine if SAML was enable
  -  or SAML was not found enabled but the target would still be vulnerable if SAML was ever enabled for it
- `not_patched`: The target is not patched but SAML is not enabled. This means the target is not currently vulnerable, but could be rendered vulnerable by enabling SAML.
- `likely_not_vulnerable`: The target does not seem vulnerable based on the performed checks.
- `unknown`: The vulnerability status could not be determined, most likely because the product version could not be obtained or was not recognized.
The script will generate a JSON file called 

## Output files
- `cve_2022_47966_scan.json` - JSON file with the product name, version, SAML configuration status, vulnerability status and other relevant information for any systems that were recognized by the script.
- `cve_2022_47966_scan.txt` - Text file with a human-readable breakdown of the results. This is identical to the report being printed to the console (minus the ANSI colors)
- `cve_2022_47966_scan_unidentified.json` - JSON file with information on systems that could not be identified, but still seem worth reporting on because the strings `ManageEngine` and/or `manageengine` were found in the response body sent by the server.

## Caveats
- The script currently uses only the self-reported build version to determine if a certain app is not patched. However, the self-reported build versions may not always be fully accurate, but they seem to give a correct indication of patch status in most cases.
- The script checks for specific strings in the server response body to see if SAML is configured for a certain app. Again, this may not always be 100% accurate, although false positives here are unlikely.
- Due to the large number of affected products, the script has been tested against a limited number of systems for each product. This may result in incorrect results for product versions that deviate from those tested. For instance, we noticed during testing that different versions of the same product sometimes present the self-reported version number in a different manner. As a result, the scanner may sometimes fail to identify the version for a product that is supported. However, in that case the scanner will still report on identifying the product and being unable to identify the version.
- In general, false negatives seem more likely than false positives.

In an attempt to provide relatively complete results despite the limitations mentioned above, the script reports on all systems, even those found not to be vulnerable as well as web apps that could be ManageEngine products but were not recognized by the script.

## So how intrusive is this thing?
The scanner is super light. For most of the supported apps, the scanner performs exactly two HTTP requests:
- A GET request to the provided URL (which should be the base URL for the app)
- An POST request with an empty body to the SAML endpoint

For a few products, one additional GET request is performed to manually follow a redirect.
For some products, the POST request is not even performed.

## Patching
Please refer to the official [ManageEngine security advisory](https://www.manageengine.com/security/advisory/CVE/cve-2022-47966.html) for a full list of affected applications and the relevant patches.

## A note on support
This scanner is provided as is. PR's and issues are welcomed, and we hope to add support for additional targets in the near future. However, we cannot guarantee support for this tool.
