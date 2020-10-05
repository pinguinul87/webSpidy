#!/usr/local/bin/python3

import re
import sys
import requests 
import optparse
import urllib.parse as urlparse

if len(sys.argv) < 2:
    print("How to use script : " + sys.argv[0] + "-t or --target_url and the URL in this format : http://URL")
    print("For more information on how to use this tool, type " + sys.argv[0] + "followed by --help")
    sys.exit(1)

parser = optparse.OptionParser()
parser.add_option("-t", "--target_url", dest="target", help="Webspider that search an entire website for hyper links - webpages, and also for files and directories.")
(values, args) = parser.parse_args()

target = values.target

def request(url):
    try:
        return requests.get(target)
    except requests.exceptions.ConnectionError:
        pass

def dir_hunter():
    with open("files-and-dirs-wordlist.txt", "r") as f:
        for line in f:
            word = line.strip()
            new_url = target + "/" + word
            response = request(new_url)
            if response:
                print("[+] URL discovered -> " + new_url)

def get_links(url):
    response = requests.get(url)
    return re.findall ('(?:href=")(.*?)"', str(response.content))

def main():
    print("="*60)
    print("[+] Fetching links from  " + target)
    print("\n")
    href_links = get_links(target)
    for link in href_links:
        link = urlparse.urljoin(target, link)
        if target in link:
            print(link)
    print("\n")
    print("[+] Fetching complete.")
    print("="*60)
    print("\n")
    print("="*60)
    print("[+] Searching for files and directories  " + target)
    print("\n")
    dir_hunter()
    print("[+] Search complete.")
    print("="*60)
main()
