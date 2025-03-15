# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 20:42:54 2025

@author: richa
"""

from chatGPT_api import get_GPT_response
from gsheet_api_readwrite import googleSheetRead, googleSheetWrite
import json
import pandas as pd

print("****STRUCTURED JSON****")
prompt = "give me 10 question-and-answer jokes, each with a comedy score out of 10. Give it in a JSON format as per the stated schema"
systemRole = "you are a joke creating bot"    
json_schema = {
                "type": "object",
                "properties": 
                    {
                    "jokes": 
                        {
                        "type": "array",
                        "items": 
                            {
                            "type": "object",
                            "properties": 
                                {
                                "jokeQuestion": {"type": "string"},
                                "jokeAnswer": {"type": "string"},
                                "comedyScore": {"type": "integer", "minimum": 1, "maximum": 10}
                                },
                            "required": ["jokeQuestion", "jokeAnswer", "score"]
                            }
                        }
                    },
                }   

data = get_GPT_response(prompt, systemRole, reponseFormat = "json_schema", json_schema = json_schema)

    
try:
    jData = json.loads(data)['jokes']
    jokes = pd.DataFrame(jData)
    print(jokes)
except:
    print("invalid json format")
