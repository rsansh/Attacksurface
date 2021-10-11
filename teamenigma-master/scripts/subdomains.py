import requests
import argparse
import datetime
import dateparser
import socket
import ssl
import sys
import urllib3
import os
urllib3.disable_warnings()
from helpers import get_request , get_certificate_expiry_date_time


DEFAULT_HTTPS_PORT = 443
SOCKET_CONNECTION_TIMEOUT_SECONDS = 10

ips = []
with open('client_list.txt','r') as f:
    for line in f:
        line = line.replace("\n", "")
        if line not in ips and len(line)>0:
             ips.append(line)

class Subdomains():

    def __init__(self):
        self.subdomains = []
        self.expiry_dates = []

    def file(self,file_output):
        with open(report_filename, "a") as fh:
            fh.write(file_output)

    def certsh(self):
        for ip in ips:
            link = "https://crt.sh/?q=%25.{}&output=json".format(ip) 
            resp = get_request(link,20)
            try:
                if resp.text and resp.status_code == 200:
                    for data in resp.json():
                        sub = data['common_name']
                        if sub not in self.subdomains:
                            self.subdomains.append(sub)
            except Exception as e:
                pass

    def sub_extractor(self,line):
        try:
            return line.split(",")[0]
        except:
            return False

    def dumpster(self):
        for ip in ips:
            link = "https://api.hackertarget.com/hostsearch/?q={}".format(ip)
            resp = get_request(link, 20)
            try:
                if resp.text and resp.status_code == 200:
                    for line in resp.text.splitlines():
                        if line.count('.') > 1:
                            sub = self.sub_extractor(line)
                            if sub in self.subdomains:
                                self.subdomains.append(sub)
            except Exception as e:
                pass

    def master(self):
        textfile = open("masterlist.txt", "w")
        textfile.truncate()
        for element in self.subdomains:
            textfile.write(element + "\n")
        print('Masterlist created')
        textfile.close()




