import sys, os
import requests
from rich import progress
from ascii import asciiart
from termcolor import colored
from configparser import ConfigParser

version = 1.06
branch = "experimental"
files = {
    "main.py" : f"https://raw.githubusercontent.com/FLINT47/pyconf/{branch}/main.py",
    "audit.py" : f"https://raw.githubusercontent.com/FLINT47/pyconf/{branch}/audit.py",
    "pastebin.py" : f"https://raw.githubusercontent.com/FLINT47/pyconf/{branch}/pastebin.py",
    "post.py" : f"https://raw.githubusercontent.com/FLINT47/pyconf/{branch}/post.py",
    "ascii.py" : f"https://raw.githubusercontent.com/FLINT47/pyconf/{branch}/ascii.py",
    "makeimg.py" : f"https://raw.githubusercontent.com/FLINT47/pyconf/{branch}/makeimg.py",
}
asciiart()
print(colored("Checking for Updates...\n", "yellow"))
r = requests.get(f"https://raw.githubusercontent.com/FLINT47/pyconf/{branch}/main.py")
with open ("check.txt", "w") as f:
    f.writelines(r.text)
with open ("check.txt", "r") as f:
    line = f.readlines()
versioncheck = line[7]
versioncheck = float(versioncheck[10:])
if versioncheck > version:
    print(colored("Updates available!!!\n", "green"))
    for fname, url in progress.track(files.items(), description="Downloading Updates"):
        r = requests.get(url)
        with open (fname, "w") as f:
            f.writelines(r.text)
    print(colored("Done\n", "green"))
else:
    print(colored("Already running the latest version\n", "green"))
os.remove("check.txt")

from makeimg import makeimg
from post import post
from audit import audit

configfile = os.path.abspath(os.path.dirname(sys.argv[0])) + "\config.cfg"
config = ConfigParser()
config.read(configfile)
postfolder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\Postings')
if not config["settings"]["audit"] == "True":
    makeimg()
    if len(os.listdir(postfolder)) == 0:
        os.rmdir(postfolder)
        input(colored(f"No new confessions found, press ENTER to Exit.", "red"))
        sys.exit(0)
    check = input(colored(f"Waiting till moderation is complete, When done press ENTER to advance to posting.\nPressing anything else will not lead to posting :", "yellow"))
    if config["settings"]["instantpost"] == "True" and config["settings"]["instantmod"] == "True" and check == "":
        post()
        sys.exit(0)
else:
    audit()

