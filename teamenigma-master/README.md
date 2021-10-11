# TeamEnigma

Process for running the script:

Step 1) Client gives their assets list / We input certain assets which we find via OSINT and we store it in the 'client_list.txt'.

Step 2) AUTODISCOVERY/SUBDOMAIN IDENTIFIER MODULE:Run the main.py(sudo python3 main.py) to fetch all the possible currently active subdomains(from cert.sh) and also the historical subdomains(DNS Dumpster, Google historical records, etc) to create a 'masterlist'.

Step 3) DOMAIN CHECKER MODULE: From the "masterlist.txt" our script will check the Domain Expiry Date and Dnssec(From WHOIS) and store it in (domain_checker.txt).

Step 4) PORT SCANNER MODULE: Port scanning(NMAP) will start automatically (uses 'masterlist.txt' as input) to get the currently active assets which are stored in the 'active_asset_list.txt'. The details of Port,Protocol and asset are stored in the 'active_asset_details.txt'

Step 5) HSTS MODULE: Each asset is checked for HSTS headers(from HTTP response) and based on the headers, further check is made for inclusion in preload list(from official google database).

Step 6) CERTIFICATE EXPIRY MODULE: Each asset is checked for the certificate expiry dates(from HTTP response).

Step 7) CIPHER MODULE: This module checks(From Mozilla Observatory) the currently supported Cipher suites for that particular assets and whether is supports different security standards such as AED and PFS.

Step 8) IP REPUTATION MODULE: Each asset is checked for blacklist listings across multiple blacklist databases(web scraping from MX-Toolbox).

Step 9) UNENCRYPTED LOGIN PAGE: Assets are checked for login forms which are being served over HTTP(checked using webscraping and HTTP response headers).

Step 10) DEFAULT WELCOME PAGE: Assets are checked(using scraping 'title' and similar tags from the HTML code) if they are matching with 10+ popular default pages(scalable). 


All the above modules save the output in a '.txt' format with the appropriate file names.
   

