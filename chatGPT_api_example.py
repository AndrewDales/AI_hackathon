# -*- coding: utf-8 -*-
from chatGPT_api import get_GPT_response
import json
import pandas as pd

# Get ChatGPT to choose a character
# Let's try the letter R
l = 'R'


#VERSION 1 - SIMPLE PROMPT
prompt = (f"Create a list of no more than 3 very famous characters, either real or fictional, beginning with the letter {l}. They must be well-known to be used to play a famous character guessing game"
          f"Use only the character's names."
          )

famous = get_GPT_response(prompt)

'''
1. Romeo  
2. Robin Hood  
3. Ronald McDonald
'''


# VERSION 2 - ADD SYSTEM ROLE AND MORE GUIDANCE ON OUTPUT
prompt = (f"Create a list of no more than 3 very famous characters, either real or fictional, beginning with the letter {l}. They must be well-known to be used to play a famous character guessing game"
          f"Use only the character's names and do not output any other information or numbering."
          )
systemRole = "you are a bot that only knows French names"    

famous = get_GPT_response(prompt, systemRole)

'''
Robin des Bois  
Raimundo  
Ratatouille
'''


# VERSION 3 - ADD REQUEST FOR JSON RESPONSE
prompt = (f"Create a list of no more than 3 very famous characters, either real or fictional, beginning with the letter {l}. They must be well-known to be used to play a famous character guessing game"
          f"Use only the character's names and do not output any other information or numbering.  Provide output in curly brackets as json eg 'characters':['Richard','Robert']"
          )
systemRole = "you are a bot that plays an online version of the 'who am i' game"    

famous = get_GPT_response(prompt, systemRole)

'''
{'characters':['Robin Hood','Ron Weasley','R2-D2']}
'''

# VERSION 3 - ADD json_schema to control output
prompt = (f"Create a list of no more than 3 very famous characters, either real or fictional, beginning with the letter {l}. They must be well-known to be used to play a famous character guessing game.  "
          f"Use only the character's names and output as json."
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
                            }
                        }
                    }
                }   
    
famous = get_GPT_response(prompt, systemRole, reponseFormat = "json_schema", json_schema = json_schema)

'''
{"characterList":[{"name":"Robin Hood"},{"name":"Ron Weasley"},{"name":"R2-D2"}]}
'''

try:
    famousList = [x['name'] for x in json.loads(famous)['characterList']]
    print(famousList)
except:
    print("error loading json")
    
    