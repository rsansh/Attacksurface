import requests
import argparse
import datetime
import dateparser
import socket
import ssl
import urllib3
from requests import get
urllib3.disable_warnings()

DEFAULT_HTTPS_PORT = 443
SOCKET_CONNECTION_TIMEOUT_SECONDS = 10

def get_request(link, timeout):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'}
    return get(link, headers=head, verify=False, timeout=timeout)


def timestamp(exp_date_text):
    date_time_str = parse_timestamp(exp_date_text)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%b-%d-%Y %I:%M%p')
    today = datetime.date.today()
    someday =date_time_obj.date()
    diff = someday - today
    return str(diff.days)
    
def parse_timestamp(ts_string):
    dt = dateparser.parse(ts_string)
    return dt.strftime("%b-%d-%Y %I:%M%p")

def get_certificate_expiry_date_time(context, host, port):
    with socket.create_connection((host, port), SOCKET_CONNECTION_TIMEOUT_SECONDS) as tcp_socket:
        with context.wrap_socket(tcp_socket, server_hostname=host) as ssl_socket:
            # certificate_info is a dict with lots of information about the certificate
            certificate_info = ssl_socket.getpeercert()
            exp_date_text = certificate_info['notAfter']
    return timestamp(exp_date_text)


