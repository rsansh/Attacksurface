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
with open('active_assets_list.txt','r') as f:
    for line in f:
        line = line.replace("\n", "")
        if line not in ips and len(line)>0:
            ips.append(line)

client = 'new'
report = '{}_report'.format(client)

report_filename = report +'/Certificate.txt'
# Create a directory named 'report' if it doesnt exist
os.makedirs(os.path.dirname(report_filename), exist_ok=True)
# Creating an empty initial summary.txt file
with open(report_filename, "w") as fh:
    fh.write("Collecting Certificate information ...")


class Expiry():

    def __init__(self):
        self.subdomains = ips

    def file(self,file_output): 
        with open(report_filename, "a") as fh:
            fh.write(file_output)

    def expirydate(self):
        file_output = "\nDomain_ip\t\t\t\t\t\tExpire_info"
        self.file(file_output)  
        for subdomain in self.subdomains:
            print(subdomain)
            try:
                res= requests.get('https://'+subdomain,verify=False)
                if res.ok == True:
                    host, _, specified_port = subdomain.partition(':')
                    port = int(specified_port or DEFAULT_HTTPS_PORT)
                    context = ssl.create_default_context()
                    date = get_certificate_expiry_date_time(context, host, port)
                    date_day = 'expires in {} days'.format(date)
                    file_output = "\n" + subdomain + "\t\t\t" + date_day 
                    self.file(file_output)
            except ssl.CertificateError as e:
                file_output = "\n" + subdomain + "\t\t\t" + str(e) 
                self.file(file_output)
            except Exception as e:
                pass
        print('Certificate Expiry for Ips completed.')
