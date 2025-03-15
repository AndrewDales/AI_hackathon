# -*- coding: utf-8 -*-
"""
https://docs.google.com/spreadsheets/d/1Hg1fvyvqoSDgN1T8AAt89o28_q-LlsuyjiNKXOborHw/edit?gid=0#gid=0

"""

# Google Sheet details
#You can get the google sheet ID from the url of your google sheet.  It looks something like this:1Hg1fvyvqoSDgN1T8AAt89o28_q-LlsuyjiNKXOborHw
#Provide this as SHEET_ID in the function call.
SHEET_ID = "1Hg1fvyvqoSDgN1T8AAt89o28_q-LlsuyjiNKXOborHw"

from gsheet_api_readwrite import googleSheetRead, googleSheetWrite, googleSheetClear
import time

def check_user_input(CELL):
    """Waits for user input A2"""
    while True:
        data = googleSheetRead(CELL, SHEET_ID=SHEET_ID)  
        if len(data)==1:  # If a non-empty cell is found
            return data[0][0]  # Return value only from list of lists
        print("no data found at",CELL,", keep checking")
        time.sleep(1)  # Wait 1 second before checking again




# Clear sheet before starting game
googleSheetClear(RANGE= "Sheet1!A1:C20", SHEET_ID = SHEET_ID)
print()

# Write to sheet
googleSheetWrite(CELL= "Sheet1!A1", VALUE="Enter the first let of the character you want me to choose into cell A2", SHEET_ID = SHEET_ID)
print()

# Read range from sheet
RANGE = "Sheet1!A1:A10"
data = googleSheetRead(RANGE, SHEET_ID=SHEET_ID)  
print("read data from", RANGE, data)
print()

# Keep reading until value exists in cell A2
CELL = "Sheet1!B2"
response = check_user_input(CELL)
print("found data at", CELL, ": ", response)
print()
