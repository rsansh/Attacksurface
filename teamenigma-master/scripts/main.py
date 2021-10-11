import domainexpiry
import certificate_expiry
import subdomains
import unencrypted_loginpage
import cipher_suite
import ip_reputation
import defaultpage_version
import portscanner
import hsts
import sys
import os



class Main():

    def __init__(self):
        pass


    def subdomains(self):
        a = subdomains.Subdomains()
        a.certsh()
        a.dumpster()
        a.master()


    def domain_checker(self):
        b = domainexpiry.Domain_Checker()
        b.get_domain()
        b.domain_expiry()
        b.domain_dnssec()

    def port_scanner(self):
        p =portscanner.Nmap()
        p.scanner()

    def hstpre(self):
        r = hsts.Hsts_preloaded()
        r.hstpre()


    def certificate_expiry(self):
        g = certificate_expiry.Expiry()
        g.expirydate()


    def cipher_cert(self):
        z = cipher_suite.Cipher()
        z.cipher_table()


    def ip_reputation(self):
        x = ip_reputation.IpReputation()
        x.blacklist()

    def unencrypted_loginpage(self):
        c = unencrypted_loginpage.Unencrypted()
        c.login_page()


    def defaultpage_version(self):
        d = defaultpage_version.Defaultpage()
        d.domain_check()
        d.title_page()



if __name__ == '__main__':
    main = Main()
    main.subdomains()
    main.domain_checker()
    main.port_scanner()
    main.hstpre()
    main.certificate_expiry()
    main.cipher_cert()
    main.ip_reputation()
    main.unencrypted_loginpage()
    main.defaultpage_version()



