#!/usr/bin/python3
import sys
import os, glob
import pandas as pd
import numpy as np
import shutil


# sorts file YEAR.csv by date and time reported then reset index
if not len(sys.argv) == 2:
    print("usage: {} [year]".format(sys.argv[0]))
    sys.exit(2)

filename = sys.argv[1] + ".csv";
df = pd.read_csv(filename, index_col=0)

df['Date Reported'] = pd.to_datetime(df['Date Reported'])
df['Date Occurred'] = pd.to_datetime(df['Date Occurred'])

df.sort_values(by = ['Date Reported', 'Time Reported'], inplace=True)
df = df.reset_index(drop=True)

to_replace = [  "BURGLARY-BREAKING & ENTERING", 
				"BURGLARYBREAKING  ENTERING",
				"COUNTERFEIT  FORGERY",
				"DESTRUCTION / VANDALISM  DAMAGE",
				"EXTORTION  BLACKMAIL",
				"FRAUD - CREDIT CARD  ATM",
				"FRAUD-FALSE PRETENSES  GAMES",
				"FRAUD-FALSE PRETENSES / GAMES",
				"FRAUD-IDENTITY THEFT",
				"INTIMIDATION/THREATENING \\(W/O WEAPON\\)",
				"INTIMIDATIONTHREATENING WO WEAPON",
				"LARCENY  ALL OTHER",
				"LARCENY-FROM BUILDING",
				"LARCENY-FROM VEHICLE",
				"LARCENY-OF M/V PARTS  ACCESSORIES",
				"LARCENY-OF M/V PARTS & ACCESSORIES",
				"LARCENY-PURSE SNATCHING",
				"LARCENY-SHOPLIFTING",
				"MOTOR VEHICLE THEFT \\(NH STEAL\\)",
				"MOTOR VEHICLE THEFT NH STEAL",
				"TOWN\\)",
				"SEX OFFENSE-FORCIBLE FONDLING",
				"DESTRUCTION/VANDALISM/DAMAGE",
				"FRAUD-CREDIT CARD/ATM",
				"INTIMIDATION/THREATENING (W/O WEAPON)",
				"LARCENY-ALL OTHER",
				"LARCENY-POCKET-PICKING"
				]
values = [      "BURGLARY - BREAKING & ENTERING", 
				"BURGLARY - BREAKING & ENTERING",
				"COUNTERFEIT / FORGERY",
				"DESTRUCTION / VANDALISM / DAMAGE",
				"EXTORTION / BLACKMAIL",
				"FRAUD - CREDIT CARD / ATM",
				"FRAUD - FALSE PRETENSES / GAMES",
				"FRAUD - FALSE PRETENSES / GAMES",
				"FRAUD - IDENTITY THEFT",
				"INTIMIDATION/THREATENING (W/O WEAPON)",
				"INTIMIDATION/THREATENING (W/O WEAPON)",
				"LARCENY - ALL OTHER",
				"LARCENY - FROM BUILDING",
				"LARCENY - FROM VEHICLE",
				"LARCENY - OF M/V PARTS & ACCESSORIES",
				"LARCENY - OF M/V PARTS & ACCESSORIES",
				"LARCENY - PURSE SNATCHING",
				"LARCENY - SHOPLIFTING",
				"MOTOR VEHICLE THEFT (NH STEAL)",
				"MOTOR VEHICLE THEFT (NH STEAL)",
				"STOLEN PROPERTY (RECOVERY FROM OTHER TOWN)",
				"SEX OFFENSE - FORCIBLE FONDLING",
				"DESTRUCTION / VANDALISM / DAMAGE",
				"FRAUD - CREDIT CARD / ATM",
				"INTIMIDATION/THREATENING (W/O WEAPON)",
				"LARCENY - ALL OTHER",
				"LARCENY - POCKET-PICKING"
				]

for i in range(len(to_replace)):
	df["Type of Incident"].replace(to_replace=to_replace[i],value=values[i],inplace=True)

df.to_csv(filename)