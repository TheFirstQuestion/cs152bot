import openai
import os
import json
from pprint import pprint
import time


class OpenAIClassifier():
    def __init__(self):
        # There should be a file called 'tokens.json' inside the same folder as this file
        token_path = 'tokens.json'
        if not os.path.isfile(token_path):
            raise Exception(f"{token_path} not found!")
        with open(token_path) as f:
            # If you get an error here, it means your token is formatted incorrectly. Did you put it in quotes?
            tokens = json.load(f)
            openai.organization = tokens["openAI_org"]
            openai.api_key = tokens['openAI_key']

    def evaluateText(self, text, pretty=False):
        # Use moderation model ()
        result = openai.Moderation.create(
            input=text,
        )
        if pretty:
            return asPercentages(result.results[0].__dict__["_previous"]["category_scores"])
        else:
            return result.results[0].__dict__["_previous"]


def asPercentages(data):
    # Iterate over the dictionary and update the values
    for key, value in data.items():
        percentage = '{:.1%}'.format(value)
        data[key] = percentage
    return data


if __name__ == "__main__":
    m = OpenAIClassifier()
    texts = ["You ugly bitch",
                    "You need to go to hell and die.",
                    "Sucker and a sore loser.",
                    "What's up, dawg?",
                    "You're spicy.",
                    "You're ridiculous.",
                    "You are a sad potato",
                    "You fucking bastard",
                    "You bloody cunt.",
                     "I'm going to kill you.",
                    "You little smelly piece of shit.",
                    "You're disgusting. I fucking hate you.",
                    "You faggot."]
    for text in texts:
        print(text)
        time.sleep(1)
        pprint(m.evaluateText(text, pretty = True))
        
    
