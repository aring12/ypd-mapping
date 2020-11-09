# ypd-mapping
Parse YPD crime log pdfs

NOTE: This code only needed to parse a couple thousand files, after which we had no more use for it.  Thus the code is rather unpolished, slow, and inefficient in places.
It is probably not usable out of the box, but with some retooling could be made to work on different PDFs, under different circumstances, etc.

FILE DESCRIPTIONS:
mod_files.py - remove extraneous files from yearly directory
parser.py - parse data from pdfs into a single pandas dataframe, export to spreadsheet.
latlong.py - get latitude and longitude data for address and add it to the dataframe/spreadsheet
sort.py - sort dataframe/spreadsheet by datetime
compile.py - compile yearly spreadsheets into a couple cumulative data tables
