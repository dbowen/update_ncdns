#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2018 Derek Bowen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import socket
import argparse
import requests
from netifaces import interfaces, ifaddresses, AF_INET

def main(argv):
    parser = argparse.ArgumentParser(description='update_ncdns')
    parser.add_argument('host', help='Host entry to update record on')
    parser.add_argument('domain', help='Domain the host entry belongs to')
    parser.add_argument('password', help='Password to update DNS record')
    args = parser.parse_args()

    # Get local ip
    local_ip = get_local_ip()
    if local_ip == None: print('No local IP'); exit()

    # Do we have a new IP address?
    last_ip = get_last_ip()
    if last_ip == local_ip: print('No IP change'); exit()

    update_dns_record(args.host, args.domain, args.password, local_ip)
    set_last_ip(local_ip)

def get_last_ip():
    try:
        with open('/tmp/update_hostname_ip', 'r') as ip_file:
            last_ip = ip_file.read()
    except:
        last_ip = None
    return last_ip

def set_last_ip(last_ip):
    with open ('/tmp/update_hostname_ip', 'w') as ip_file:
        ip_file.write(last_ip)

def get_local_ip():
    addresses = list()
    for interface in interfaces():
        addresses.extend([i['addr'] for i in ifaddresses(interface).setdefault(AF_INET, [{'addr': 'No IP addr'}])])
    addresses = [a for a in addresses if a != 'No IP addr' and a != '127.0.0.1']
    return addresses[0] or None

def update_dns_record(host, domain, password, ip):
    url = 'https://dynamicdns.park-your-domain.com/update'
    params = {'host': host, 'domain': domain, 'password': password, 'ip': ip}
    response = requests.get(url, params=params)

if __name__ == "__main__":
    main(sys.argv[1:])
