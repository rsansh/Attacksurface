import requests
import settings
import sys
import os
import socket
from helpers import get_request
import urllib3
urllib3.disable_warnings()


ips = []
with open('active_assets_list.txt','r') as f:
    for line in f:
        line = line.replace("\n", "")
        if line not in ips and len(line)>0:
            ips.append(line)

client = 'new'

report = '{}_report'.format(client)

report_filename = report +'/uncrypted_loginpage.txt'
# Create a directory named 'report' if it doesnt exist
os.makedirs(os.path.dirname(report_filename), exist_ok=True)
# Creating an empty initial summary.txt file
with open(report_filename, "w") as fh:
    fh.write("Collecting Uncrypted_loginpage ...")

class Unencrypted():

    def __init__(self):
        self.present = []
        self.not_present = []

    def file(self,file_output):
        with open(report_filename, "a") as fh:
            fh.write(file_output)

    def redirect(self,ip):
        try:
            res = requests.get('http://'+ip,verify=False)
        except Exception as e:
            res = None
        return res

    def check(self,ip):
        get_url = self.redirect(ip)
        if get_url:
            get_url = get_url.url
            get_ip = get_url.split('//')[1]
            want = 'http://'+ get_ip
            if want in get_url:
                return want

    def login_page(self):
        file_output = "\nDomain_ip\t\t\t\t\t\t\t\t\tResult"
        self.file(file_output)
        for ip in ips:
            check_ip = self.check(ip)
            if check_ip == None:
                pass
            else:
                res = get_request(check_ip,5)
                if res.is_redirect == False:
                    find_text = res.text
                    for text in settings.master_list:
                        if text in find_text:
                            self.present.append(text)
                    if len(self.present) > 0:
                        file_output = "\n" + check_ip + "\t\t\t" + 'Uncrypted Login Page Present' 
                        self.file(file_output)
        print('Unecrypted Login page Completed.')
