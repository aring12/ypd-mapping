#!/usr/bin/python3
import os, glob
import sys
import shutil
import pandas as pd
import numpy as np
import tabula
import re
import zlib

# NOTE: does not work for multiple page documents so far - if there are any of these the
# second page will have to be parsed by hand

if not len(sys.argv) == 2:
    print("usage: {} [year]".format(sys.argv[0]))
    sys.exit(2)

path = "/Users/Adin/Desktop/ypd mapping/YPD Crime Logs/" + sys.argv[1] + "/"
logs = glob.glob(os.path.join(path, "*"))
dataFrames = pd.DataFrame()

# regular expressions
stream = re.compile(b'.*?FlateDecode.*?stream(.*?)endstream', re.S)
raw_text = re.compile(r'Disposition(.*).\(Page', re.S)
text = re.compile(r'[^j]\n.*?\((.*)\) Tj(\s\[(.*)\] TJ)?')

j=0
# parse all logs, read them into data frames, and append them to merged
num_logs = len(logs)
for f in logs:
    j += 1
    print("{} ({} / {})".format(f,j,num_logs))
    pdf = open(f, "rb").read()

    # look for first bytestream in pdf and trim it
    s = re.search(stream, pdf).group(1)
    s = s.strip(b'\r\n')
    # decompress bytestream
    try:
        s = zlib.decompress(s).decode('UTF-8')
    except (UnicodeDecodeError, zlib.error):
        shutil.move(f, "/Users/Adin/Desktop/ypd mapping/failures/")
        print("Couldn't decode for file: {}, moved to failures".format(f))
        continue
    # search for raw text
    text_strings = re.search(raw_text, s)
    raw = text_strings.group(1)
    # finds all text within raw text and adds it to a list
    text_list = []
    array_size = 0
    for t in re.findall(text, raw):
        string = t[0] + "".join(re.findall("[a-zA-Z ]+", t[2]))
        if string != "NO INCIDENTS TO REPORT":
            #print(string)
            text_list.append(string)
            if string == "Arrest" or string == "Active" or string == "Closed" or string == "Unknown":
                array_size += 1
    # skip the no incident reports
    if array_size == 0:
        continue
    # iterates through text_list putting data into a dataframe
    df = pd.DataFrame(columns=['Date Reported', 'Time Reported', 'Type of Incident', 'Date Occurred',
                               'Time Occurred', 'Location', 'Disposition'])
    i = 0
    row = 0
    try:
        while i + 5 < len(text_list):
            # First row should start with a capital letter, second with a number
            # --> if this isn't true, just augment i and try again
            if not text_list[i][0].isupper() or not text_list[i+1][0].isdigit():
                i += 1
                continue
            new_row = [None]*7
            new_row[2] = text_list[i]
            new_row[0] = text_list[i+1].split("  ")[0]
            new_row[1] = text_list[i+1].split("  ")[1]
            new_row[3] = text_list[i+2].split("  ")[0]
            new_row[4] = text_list[i+2].split("  ")[1]
            new_row[5] = text_list[i+3]
            if text_list[i + 5] in ["Arrest", "Active", "Closed"]:
                new_row[6] = text_list[i + 5]
                i += 6
                if i < len(text_list) and text_list[i][0].isdigit():
                    i += 1
            elif i + 6 < len(text_list) and text_list[i + 6] in ["Arrest", "Active", "Closed"]:
                new_row[6] = text_list[i + 6]
                i += 7
            df.loc[row] = new_row
            row += 1
        # add df to total frame
        dataFrames = dataFrames.append(df, ignore_index=True, sort=False)
    # file couldn't be parsed, move it to failures and keep on going
    except IndexError:
        shutil.move(f, "/Users/Adin/Desktop/ypd mapping/failures/")
        print("moved {} to failures".format(f))
        continue
print(dataFrames)
dataFrames.to_csv(sys.argv[1] + ".csv")

# if append_supplements:
#     # read all supplements into data frames and append them to merged
#     for f in supplements:
#         dfs = tabula.read_pdf(f, pages='all')
#         if len(dfs) == 0:
#             print("empty")
#             continue
#         df = dfs[0].replace({'\r': ' '}, regex=True)
#         df = df.replace({'‐': '-'}, regex=True)
#         df = df.drop(["Case Number"], axis=1)
#         dataFrames = dataFrames.append(df, ignore_index=True, sort=False)
#         break