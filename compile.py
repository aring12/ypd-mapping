#!/usr/bin/python3
import os, glob
import pandas as pd

path = "/Users/Adin/Desktop/ypd mapping/finished/"
finished = glob.glob(os.path.join(path, "*.csv"))

dataFrames = pd.DataFrame()

#compile files into one dataframe
for f in finished:
	print(f)
	df = pd.read_csv(f, index_col=0)
	dataFrames = dataFrames.append(df, ignore_index=True, sort=False)

dataFrames['Date Reported'] = pd.to_datetime(dataFrames['Date Reported'])
dataFrames['Date Occurred'] = pd.to_datetime(dataFrames['Date Occurred'])

dataFrames = dataFrames.sort_values(by = ['Date Reported', 'Time Reported'])
dataFrames = dataFrames.reset_index(drop=True)

all_arrests = dataFrames[dataFrames['Disposition'] == 'Arrest']
all_arrests = all_arrests.reset_index(drop=True)

dataFrames.to_csv("./finished/alltime.csv")
all_arrests.to_csv("./finished/allarrests.csv")