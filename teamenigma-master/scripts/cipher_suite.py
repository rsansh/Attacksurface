import requests
import sys
import json
import os
import urllib3
import certifi
from urllib3 import PoolManager, Timeout
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ConnectionError
from selenium import webdriver
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



ips = []
with open('active_assets_list.txt','r') as f:
    for line in f:
        line = line.replace("\n", "")
        if line not in ips and len(line)>0:
            ips.append(line)

client = 'new'

report = '{}_report'.format(client)

report_filename = report +'/certificate_cipher.txt'
# Create a directory named 'report' if it doesnt exist
os.makedirs(os.path.dirname(report_filename), exist_ok=True)
# Creating an empty initial summary.txt file
with open(report_filename, "w") as fh:
    fh.write("Collecting Domian Certificate Cipher ...")


class Cipher():

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(executable_path=r"chromedriver",options=self.options)

    def file(self,file_output): 
        with open(report_filename, "a") as fh:
            json.dump(file_output, fh)


    def cipher_table(self):
        try:
            for ip in ips:
                print(ip)
                self.driver.get('https://observatory.mozilla.org/analyze/{}#tls'.format(ip))
                table = WebDriverWait(self.driver,10).until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr')))
                self.cipher_details(table,ip)
        except Exception as e:
            print('Table not found for {}'.format(ip))


    def cipher_details(self,table,ip):
        result = []
        rslt =[]
        for i in table:
            temp_record = {}
            rtr = i.text
            sp = rtr.split()
            temp_record['Domain'] = ip
            temp_record['Cipher_suite'] = sp[0]
            temp_record['Code'] = sp[1] +'/'+ sp[2]
            temp_record['Key_Size'] = sp[3] +' '+ sp[4]
            temp_record['Protocols'] = sp[5] +' '+ sp[6]
            result.append(temp_record)


        row = len(table)
        for tr in range(1,row+1):
            temp_record ={}
            aed = self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(tr)+"]/td[4]/span[@class='tablesaw-cell-content']//*[local-name()='svg']/*[local-name()='path']").get_attribute('d')
            aed_len = len(aed)
            if aed_len < 100:
                aead_ = 'Yes'
            else:
                aead_ = 'No'

            pfs = self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr["+str(tr)+"]/td[5]/span[@class='tablesaw-cell-content']//*[local-name()='svg']/*[local-name()='path']").get_attribute('d')
            pfs_len = len(pfs)
            if pfs_len < 100:
                pfs_ = 'Yes'
            else:
                pfs_ = 'No'

            temp_record['AEAD'] = aead_
            temp_record['PFS'] =  pfs_
            rslt.append(temp_record)

        for value in range(0,len(result)):
            result[value].update(rslt[value])

        print(result)
        file_output = result
        self.file(file_output)

        print('Cipher Suite for Certificate Completed.')
