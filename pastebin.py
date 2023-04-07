import requests 
from xml.etree import ElementTree as ET
from configparser import ConfigParser
import os
import sys


configfile = os.path.abspath(os.path.dirname(sys.argv[0])) + "\config.cfg"
config = ConfigParser()
config.read(configfile)
api_dev_key = config["account"]["api_dev_key"]
api_user_key = config["account"]["api_user_key"]
if not(os.path.exists(os.path.abspath(os.path.dirname(sys.argv[0])) + "\pastebin.xml")):
    with open(os.path.abspath(os.path.dirname(sys.argv[0])) + "\pastebin.xml", "x") as fp:
        pass
def saveidx(index):
    paste_data = {
        'api_option' : 'paste',
        'api_dev_key' : api_dev_key,
        'api_paste_code' : index,
        'api_paste_name' : "index",
        'api_paste_expire_date' : 'N',
        'api_user_key' : api_user_key,
        'api_paste_private' : '2'
        }
    requests.post("https://pastebin.com/api/api_post.php", data=paste_data)
def loadidx():
    list_data = {
        'api_option' : 'list',
        'api_user_key' : api_user_key,
        'api_dev_key' : api_dev_key,
        }
    r = requests.post("https://pastebin.com/api/api_post.php", data=list_data)
    with open("pastebin.xml", "w") as fp:
        fp.write(r.text)
    tree = ET.parse("pastebin.xml")
    root = tree.getroot()
    api_paste_key = root[0].text
    read_data = {
        'api_option' : 'show_paste',
        'api_user_key' : api_user_key,
        'api_dev_key' : api_dev_key,
        'api_paste_key' : api_paste_key,
        }
    r = requests.post("https://pastebin.com/api/api_raw.php", data=read_data)
    return r.text
def deleteidx():
    tree = ET.parse("pastebin.xml")
    root = tree.getroot()
    api_paste_key = root[0].text
    delete_data = {
        'api_option' : 'delete',
        'api_paste_key' : api_paste_key,
        'api_user_key' : api_user_key,
        'api_dev_key' : api_dev_key,
        }
    requests.post("https://pastebin.com/api/api_post.php", data=delete_data)

if __name__ == "__main__":
    n = input("1. Retreive Current Index\n2. Update Index\nEnter your Choice: ")
    if n == "1":
        print(loadidx())
    elif n == "2":
        oldidx = int(loadidx())
        n = int(input("Enter the New Index: "))
        if n >= oldidx:
            print("New Index can't be greater than Old Index. Try again!!")
        else:
            deleteidx()
            saveidx(n)
            print("Done")
    else:
        print("Wrong Input try again.")