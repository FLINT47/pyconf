import os
import pandas as pd
import photoshop.api as ps
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from cleantext import clean
import sys
from configparser import ConfigParser
from thefuzz import fuzz
from termcolor import colored
from rich import progress
from ascii import asciiart
from post import post
from audit import audit
import regex

def main():
    asciiart()
    banned_user = (config["settings"]["bannedUser"]).split(", ")
    id = config["account"]["id"]
    if config["settings"]["load"] == "True":
        print(colored(f"Automatic download is enabled in the config...\n\nAutomatically downloading the latest confessions...\n", "cyan"))
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        file_obj = drive.CreateFile({'id':id})
        file_obj.GetContentFile('Confessions.csv',mimetype='text/csv')
        print(colored(f"Done!!\n", "green"))
    else:
        print(colored(f"Confessions weren't updated, using the old ones...\n\nYou can chnage this behaviour in the config.cfg file.\n", "cyan"))
    if config["settings"]["auto"] == "True":
        print(colored(f"Auto index is enabled, retreiving last posted confession.\n", "cyan"))
        n = int(config["index"]["form"]) + 1
    else:
        while True:
            conf_num = input(colored("Auto loading of index is disabled in config file, please enter the confession number :", "cyan"))
            if conf_num.isdigit():
                n = int(conf_num) + 1
                break
            else:
                conf_num = input("Wrong Input, try Again: ")
    condata = pd.read_csv("Confessions.csv", header = 1,  skiprows = [i for i in range(2,n)])
    con_list = []
    for _, rows in condata.iterrows():
        temp_list =[rows.Gender, rows.Proff, rows.Victim, rows.Confession, rows.Time]
        con_list.append(temp_list)
    length = len(con_list)
    app = ps.Application()
    bkg_path = os.path.abspath(os.path.dirname(sys.argv[0])) + "\Background.psd"
    app.load(bkg_path)
    file = app.activeDocument
    head_layer = file.artLayers["Head"]
    body_layer = file.artLayers["Body"]
    if not(os.path.exists(postfolder)):
        os.mkdir(postfolder)
    def isbanned(user):
        for i in banned_user:
            if fuzz.ratio(user, i) > 60:
                return True
    for i in progress.track(range(0,length), description="Generating Images"):
        gender = str(con_list[i][0])
        gender = gender.replace("\n"," ")
        if gender == "Male":
            gender = "A Boy from "
        elif gender == "Female":
            gender = "A Girl from "
        elif gender == "":
            gender = "Someone from "
        elif gender == "Rather Not Say":
            gender = "Someone from "
        else:
            gender = gender + " from "
        proff = con_list[i][1]
        proff = proff.replace("\n"," ")
        if proff == "Intern":
            gender = ""
            proff = "An Intern"
        elif proff == "Rather Not Say":
            gender = "Someone"
            proff = ""
        victim = con_list[i][2]
        victim = victim.replace("\n"," ")
        confession = con_list[i][3].strip()
        confession = confession.replace("\n"," ")
        confession = clean(confession, no_emoji=True, fix_unicode=False, to_ascii=False, lower=False)
        time = con_list[i][4]
        timestamp = time.split(' ')
        date = timestamp[0].replace('/', '-')
        time = timestamp[1]
        time = time[:-3]
        time = time.replace(':', 'h ') + 'm.'
        filename = date + ' ' + time
        header_text = gender + proff + " confesses to " + victim
        body_text = confession
        if config["settings"]["verbose"] == "True":
            print (header_text)
            print (body_text + f"\n\n")
        c = 0
        font_sizes = [250, 232, 214, 208, 208, 196, 188, 182, 180, 178, 170, 168, 166, 162, 158, 156, 150, 148, 148, 144, 142, 140, 136, 132, 132, 130]
        head_layer.textItem.size = 310
        tolerance = 0
        if bool(regex.match(r'\p{Bengali}+', body_text)):
            tolerance = 150
        if len(header_text) > 90:
            head_layer.textItem.size = 250
        if len(body_text) <= 350:
            for j in range(0, 350, 35):
                if len(body_text) > j:
                    if c <= 4:
                        depth = (2355 - tolerance) - 90 * c
                    else:
                        depth = (1300 - tolerance) + 120 * (10 - c)
                    c += 1
            body_layer.textItem.size = 250
            body_layer.textItem.position = [395, depth]
        elif len(body_text) > 350:
            for k in range(350, 1225, 35):
                if k >= len(body_text):
                    break
                c += 1
            font_size = font_sizes[c]
            body_layer.textItem.size = font_size
            depth = 1500 - tolerance
            body_layer.textItem.position = [395, depth]
        if isbanned(victim):
            print(colored(f"The user {victim} is in the banned list, confession skipped...\n", "red"))
        else:
            head_layer.textItem.contents = header_text
            body_layer.textItem.contents = body_text
            options = ps.JPEGSaveOptions(quality=12)
            jpg_file = os.path.join(postfolder, f"{filename}.jpg")
            file.saveAs(jpg_file, options, asCopy=True)
            if config["settings"]["instantmod"] == "True":
                os.startfile(jpg_file)
        if config["settings"]["load"] == "True":
            re_index = int(config["index"]["form"]) + 1
            config.set("index", "form", str(re_index))
            with open(configfile, 'w') as f:
                config.write(f)
    print (colored(f"Done!!\n", "green"))
    # input(f"Press Enter to Quit.")

if __name__ == "__main__":
    configfile = os.path.abspath(os.path.dirname(sys.argv[0])) + "\config.cfg"
    config = ConfigParser()
    config.read(configfile)
    postfolder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\Postings')
    if not config["settings"]["audit"] == "True":
        main()
        if len(os.listdir(postfolder)) == 0:
            os.rmdir(postfolder)
            print(colored("No new Confessions, Exitting...", "red"))
            sys.exit(0)
        check = input(colored(f"Waiting till moderation is complete, When done press ENTER to advance to posting.\nPressing anything else will not lead to posting :", "yellow"))
        if config["settings"]["instantpost"] == "True" and config["settings"]["instantmod"] == "True" and check == "":
            post()
            sys.exit(0)

    else:
        audit()