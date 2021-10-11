import requests
import re
import settings
import sys
import os
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

report_filename = report +'/defaultpage.txt'
# Create a directory named 'report' if it doesnt exist
os.makedirs(os.path.dirname(report_filename), exist_ok=True)
# Creating an empty initial summary.txt file
with open(report_filename, "w") as fh:
    fh.write("Collecting Defaultpage ...")


class Defaultpage():

    def __init__(self):
        self.domainlist = []
        self.port = ['https://','http://']

    def file(self,file_output): 
        with open(report_filename, "a") as fh:
            fh.write(file_output)

    def domain_check(self):
        file_output = "\nDomain_ip\t\t\t\t\tResult"
        self.file(file_output)
        for protocol in self.port:
            for domain in ips:
                try:
                    res = get_request(protocol+domain,5)
                    if res.ok == True:
                        self.domainlist.append(domain)
                except Exception as e:
                    print(e)

    def title_page(self):
        for protocol in self.port:
            for domain in self.domainlist:
                try:
                    res = get_request(protocol+domain,5)
                    text = res.text
                    result = re.search(r'(?<=title>).*(?=</title>)',text)
                    if result:
                        check_result = result.group(0) 
                        print(domain,check_result)
                        check_data  = [check for check in settings.dafaultpage_list if(check in check_result)]
                        if len(check_data) > 0:
                            file_output = "\n" + domain + "\t\t\t" + check_result
                            self.file(file_output)
                except Exception as e:
                    pass
        print('Default Page Completed')





