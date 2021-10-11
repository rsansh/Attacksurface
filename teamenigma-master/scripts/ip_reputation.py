import re
from time import sleep
import requests
import socket
import settings
import os
import sys
from selenium import webdriver
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

report_filename = report +'/ip_reputation.txt'
# Create a directory named 'report' if it doesnt exist
os.makedirs(os.path.dirname(report_filename), exist_ok=True)
# Creating an empty initial summary.txt file
with open(report_filename, "w") as fh:
    fh.write("Collecting IpReputation ...")


class IpReputation():

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(executable_path=r"chromedriver",options=self.options)

    def file(self,file_output):
        with open(report_filename, "a") as fh:
            fh.write(file_output)


    def blacklist(self):
        file_output = "\nDomain_ip\t\t\t\tBlacklist"
        self.file(file_output)

        try:
            for ip_ in ips:
                print(ip_)
                ip = socket.gethostbyname(ip_)
                self.driver.get(settings.link.format(ip))
                sleep(7)

                table = self.driver.find_element_by_xpath(settings.table).text
                data = table.split('\n')

                for rep in data:
                    if 'LISTED' in rep:  
                        spam = re.search(r'(?<=LISTED).*(?= \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',rep).group(0)
                        file_output = "\n" + ip+' ('+ip_+') ' + "\t\t\t" + spam 
                        self.file(file_output)
            print('Ip Reputation Completed.')
        except Exception as e:
            pass





