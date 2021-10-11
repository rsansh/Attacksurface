import whois
import re
import sys
import os
import urllib3
urllib3.disable_warnings()


ips = []
with open('masterlist.txt','r') as f:
    for line in f:
        line = line.replace("\n", "")
        if line not in ips and len(line)>0:
            ips.append(line)


report = '{}_report'.format('new')

report_filename = report +'/domian_checker.txt'
# Create a directory named 'report' if it doesnt exist
os.makedirs(os.path.dirname(report_filename), exist_ok=True)
# Creating an empty initial summary.txt file
with open(report_filename, "w") as fh:
    fh.write("Collecting Domain Info ...")

class Domain_Checker():

    def __init__(self):
        self.domainlist = []

    def file(self,file_output): 
        with open(report_filename, "a") as fh:
            fh.write(file_output)


    def get_domain(self):
        for domain in ips:
            check_domain = re.match(r'\w+[.]\w+$',domain)
            if check_domain:
                self.domainlist.append(check_domain.group(0))

    def domain_expiry(self):
        file_output = "\nDomain_ip\t\t\t\tExpiry_datetime"
        self.file(file_output)
        for domain in self.domainlist:
            whois_info = whois.whois(domain)
            expiry_date = whois_info.expiration_date
            if type(expiry_date) == list:
                file_output = "\n" + domain + "\t\t\t" + str(expiry_date[0])
                self.file(file_output)
            else: 
                file_output = "\n" + domain + "\t\t\t" + str(expiry_date)
                self.file(file_output)

#            print(domain,whois_info.expiration_date)

    def domain_dnssec(self):
        file_output = "\nDomain_ip\t\t\t\tDnsSec"
        self.file(file_output)
        for domain in self.domainlist:
            whois_info = whois.whois(domain)
            dnssec = whois_info.dnssec
            if type(dnssec) == str:
                file_output = "\n" + domain + "\t\t\t" + dnssec
                self.file(file_output)
            elif type(dnssec) == list:
                file_output = "\n" + domain + "\t\t\t" + dnssec[0]
                self.file(file_output)

        print('Domain Expiry and Dnsec completed')









