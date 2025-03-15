# -*- coding: utf-8 -*-
"""
https://docs.google.com/spreadsheets/d/1Hg1fvyvqoSDgN1T8AAt89o28_q-LlsuyjiNKXOborHw/edit?gid=0#gid=0

"""

#specify your google sheet ID here:
SHEET_ID = "1Hg1fvyvqoSDgN1T8AAt89o28_q-LlsuyjiNKXOborHw"

from chatGPT_api import get_GPT_response
from gsheet_api_readwrite import googleSheetRead, googleSheetWrite, googleSheetClear
import json
import pandas as pd
import time

def check_user_input(attempts):
    """Waits for user input in the next empty cell of column A"""
    startingRow = 3
    row = startingRow + attempts
    while True:
        data = googleSheetRead("Sheet1!A"+str(row), SHEET_ID=SHEET_ID)  # Read from A3 downwards
        if len(data)==1:  # If a non-empty cell is found
            return data[0][0]  # Return value and row index (A3 corresponds to index 3)
        time.sleep(1)  # Wait 1 second before checking again

def provide_user_response(response, attempts):
    startingRow = 3
    row = startingRow + attempts
    googleSheetWrite(CELL=f"Sheet1!B{row}", VALUE=response, SHEET_ID=SHEET_ID)



# Clear sheet before starting game
googleSheetClear(RANGE= "Sheet1!A1:C20", SHEET_ID = SHEET_ID)
googleSheetWrite(CELL= "Sheet1!A1", VALUE="Enter the first let of the character you want me to choose into cell A2", SHEET_ID = SHEET_ID)

l = check_user_input(-1)

# Get ChatGPT to choose a character
seed_value = int(time.time()) % 1000  # Use the current time as a seed
print("seed value", seed_value)
prompt = (f"Create a list of no more than 3 very famous characters, either real or fictional, beginning with the letter {l}. They must be well-known to be used to play a famous character guessing game"
          f"Use only the character's names and output as json.  Use {seed_value} to randomise your selection."
          )
systemRole = "you are a bot that plays an online version of the 'who am i' game"    

json_schema = {
                "type": "object",
                "properties": 
                    {
                    "characterList": 
                        {
                        "type": "array",
                        "items": 
                            {
                            "type": "object",
                            "properties": 
                                {
                                "name": {"type": "string"},
                                },
                            "required": ["jokeQuestion", "jokeAnswer", "score"]
                            }
                        }
                    }
                }   
    
famous = get_GPT_response(prompt, systemRole, reponseFormat = "json_schema", json_schema = json_schema)

try:
    famousList = [x['name'] for x in json.loads(famous)['characterList']]
    select = int(time.time()) % len(famousList)
    famous = famousList[select]
    print(famous)
except:
    print("error loading json")
    
    
    
googleSheetWrite(CELL= "Sheet1!A1", VALUE="My name begins with "+famous[0], SHEET_ID=SHEET_ID)
googleSheetWrite(CELL= "Sheet1!A2", VALUE="Enter your Yes/No question below", SHEET_ID=SHEET_ID)


# Initialize game variables
max_attempts = 10
attempts = 0
user_guess = ""


# Start guessing game
while attempts < max_attempts:
    print("attempt number", attempts)
    user_question = check_user_input(attempts)
    print("user question retrieved", user_question)
    # Ask ChatGPT to respond with Yes/No
    prompt = (f"We are playing the guessing game 'Who am I'. The character is {famous}. "
              "Answer the following question with only 'Yes', 'No', 'I don't know' or 'You Win' (without a period)"
              "Answer you win if the user guesses the characer correctly.  Allow a little flexibility for variation and misspellings and ignore capitalization.  eg if the answer is Spongebob Squarepants, accept as a winning question 'Are you spongebob?', 'sponge bob', 'is it spongbob square panst', 'you SPONGEBB'"
              f"The user's question is: {user_question}")
    
    response = get_GPT_response(prompt, systemRole, reponseFormat = "text")
    
    # Write the response in the next column
    provide_user_response(response, attempts) 
    
    # Check if user guessed the character
    if (famous.lower() in user_question.lower()) or ('you win' in response.lower()):
        googleSheetWrite(CELL="Sheet1!C3", VALUE=f"Congratulations! You guessed {famous} correctly!", SHEET_ID=SHEET_ID)
        break
    
    attempts += 1

# Game over message if not guessed
if attempts == max_attempts:
    googleSheetWrite(CELL="Sheet1!C3", VALUE=f"Game over! The correct answer was {famous}.", SHEET_ID=SHEET_ID)


