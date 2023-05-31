import openai
import os
import json
from pprint import pprint


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

    def evaluateText(self, text):
        # Use moderation model (https://platform.openai.com/docs/api-reference/moderations?lang=python)
        result = openai.Moderation.create(
            input=text,
        )
        return result.results[0].__dict__["_previous"]


if __name__ == "__main__":
    m = OpenAI()
    pprint(m.evaluateText("I think you're ugly"))
