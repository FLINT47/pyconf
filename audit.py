import os
import pandas as pd
import photoshop.api as ps
from cleantext import clean
import sys
from ascii import asciiart
import regex


def audit():
    app = ps.Application()
    bkg_path = os.path.abspath(os.path.dirname(sys.argv[0])) + "\Background.psd"
    app.load(bkg_path)
    file = app.activeDocument
    head_layer = file.artLayers["Head"]
    body_layer = file.artLayers["Body"]
    conf_num = int(input("Enter Confession Number: "))
    conf_num -= 1
    condata = pd.read_csv("Confessions.csv", header = 1)
    single_conf = condata.loc[[conf_num],:]
    for _, rows in single_conf.iterrows():
        confession = [rows.Gender, rows.Proff, rows.Victim, rows.Confession]
    print(confession)
    gender = confession[0]
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
    proff = confession[1]
    proff = proff.replace("\n"," ")
    if proff == "Intern":
        gender = ""
        proff = "An Intern"
    elif proff == "Rather Not Say":
        gender = "Someone"
        proff = ""
    victim = confession[2]
    victim = victim.replace("\n"," ")
    confessionT = confession[3].strip()
    confessionT = confessionT.replace("\n"," ")
    confessionT = clean(confessionT, no_emoji=True, fix_unicode=False, to_ascii=False, lower=False)
    header_text = gender + proff + " confesses to " + victim
    body_text = confessionT
    c = 0
    font_sizes = [250, 232, 214, 208, 208, 196, 188, 182, 180, 178, 170, 168, 166, 162, 158, 156, 150, 148, 148, 144, 142, 140, 136, 132, 132, 130]
    head_layer.textItem.size = 300
    tolerance = 0
    if len(header_text) > 90:
        head_layer.textItem.size = 250
    if bool(regex.match(r'\p{Bengali}+', body_text)):
        tolerance = 200
    if len(body_text) <=350:
        for j in range(0, 350, 35):
            if len(body_text) > j:
                if c <=4:
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
    head_layer.textItem.contents = header_text
    body_layer.textItem.contents = body_text


if __name__ == "__main__":
    asciiart()
    audit()