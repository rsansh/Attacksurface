import requests
import sys
import os
import urllib3
import certifi
import settings
from urllib3 import PoolManager, Timeout
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ConnectionError
from selenium import webdriver
from time import sleep
from helpers import get_request
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

client = 'new'

report = '{}_report'.format(client)

report_filename = report +'/hsts_preloaded.txt'
# Create a directory if it doesnt exist
os.makedirs(os.path.dirname(report_filename), exist_ok=True)
# Creating an empty initial file
with open(report_filename, "w") as fh:
    fh.write("Collecting Hsts and Preloaded info ...")

ips = []
with open('active_assets_list.txt','r') as f:
    for line in f:
        line = line.replace("\n", "")
        if line not in ips and len(line)>0:
            ips.append(line)


class Hsts_preloaded():

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(executable_path=r'chromedriver',options=self.options)


    def file(self,file_output): 
        with open(report_filename, "a") as fh:
            fh.write(file_output)



    def scrape(self,ip):
        self.driver.get('https://hstspreload.org/?domain={}'.format(ip))
        sleep(5)
        status = self.driver.find_element_by_id('status').text
        status = status.strip('Status:')
        return status



    def hstpre(self):
        file_output = "\nDomain\t\t\t\t\tHsts\t\t\tPreloaded"
        self.file(file_output)
        for url in ips:
            print(url)
            try:
                check = get_request('https://'+url,2)
                response=check.headers
                if 'Strict-Transport-Security' in response:
                    if response['Strict-Transport-Security'].split()[-1] == 'preload':
                        check = self.scrape(url)
                        if 'currently preloaded' in check:
                            file_output = "\n" + url + "\t\t\t" + 'Yes' + "\t\t\t" + 'Yes'
                            #print(file_output)
                            self.file(file_output)
                        else:
                            file_output = "\n" + url + "\t\t\t" + 'Yes' + "\t\t\t" + 'No'
                            #print(file_output)
                            self.file(file_output)
                    else:
                        file_output = "\n" + url + "\t\t\t" + 'Yes' + "\t\t" + 'No'
                        #print(file_output)
                        self.file(file_output)
                else:
                    file_output = "\n" + url + "\t\t\t" + 'No' + "\t\t" + 'No'
                    #print(file_output)
                    self.file(file_output)

            except Exception as e:
                pass
        print("Hsts and Preloaded Check Completed.")

