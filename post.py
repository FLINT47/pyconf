from instagrapi import Client
import os
import time
from configparser import ConfigParser
import sys
import base64
from termcolor import colored
from ascii import asciiart
from rich import progress


def post():
    try:
        configfile = os.path.abspath(os.path.dirname(sys.argv[0])) + "\config.cfg"
        instaconfig = os.path.abspath(os.path.dirname(sys.argv[0])) + "\settings.json"
        config = ConfigParser()
        config.read(configfile)
        password = config["account"]["password"]
        encbytes = password.encode("ascii")
        dencstr = base64.b64decode(encbytes)
        realpass = dencstr.decode("ascii")
        cl = Client()
        if os.path.exists(instaconfig):
            cl.load_settings("settings.json")
            cl.login("confessions_nrsmc", realpass)
        else:
            cl.login("confessions_nrsmc", realpass)
            cl.dump_settings("settings.json")
        upload_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Postings/')
        count = 0
        for path in os.listdir(upload_folder):
            if os.path.isfile(os.path.join(upload_folder, path)):
                count += 1
        n = 1
        for img in progress.track(os.listdir(upload_folder)):
            suffix = "a.m."
            timestamp = (os.path.splitext(os.path.basename(upload_folder + img))[0])
            date = timestamp[:10]
            hr = int(timestamp[11:13])
            min = timestamp[14:16]
            if hr > 12:
                hr = hr - 12
                suffix = "p.m."
            elif hr == 0:
                hr = 12
            if hr < 10:
                hr = "0"+ str(hr)
            caption = f"Confession Submitted on {date}, {hr}:{min} {suffix}\n.\n.\n.\nWanna Confess something? Visit the link in Bio."
            print(colored(f"Posting Confession Number {n} out of {count}.", "cyan"))
            cl.photo_upload(upload_folder + img, caption)
            print(colored(f"Confession Posted.\n", "green"))
            os.remove(upload_folder + img)
            time.sleep(1)
            n += 1
        os.rmdir(upload_folder)
        print(colored(f"Done!!\n", "green"))
    except Exception as e:
        print("An error occurred")
        print(str(e))
    input(colored(f"Press ENTER to Exit.", "yellow"))
        

if __name__ == "__main__":
    asciiart()
    post()