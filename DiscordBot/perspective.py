import os
import json
from googleapiclient import discovery
from pprint import pprint


class PerspectiveClassifier():
    def __init__(self):
        # There should be a file called 'tokens.json' inside the same folder as this file
        token_path = 'tokens.json'
        if not os.path.isfile(token_path):
            raise Exception(f"{token_path} not found!")
        with open(token_path) as f:
            # If you get an error here, it means your token is formatted incorrectly. Did you put it in quotes?
            tokens = json.load(f)

            self.client = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=tokens["google"],
                discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                static_discovery=False,
            )

    def evaluateText(self, text, pretty=True, threshold=0.8):
        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {},
                                    "SEVERE_TOXICITY": {},
                                    "IDENTITY_ATTACK": {},
                                    "INSULT": {},
                                    "PROFANITY": {},
                                    "THREAT": {}}
        }

        response = self.client.comments().analyze(body=analyze_request).execute()

        if pretty:
            cleaned = {}
            # daniel: adding whether it's generally toxic '_flagged'
            cleaned["flagged"] = False
            for category in response["attributeScores"]:
                cleaned[category.lower(
                )] = response["attributeScores"][category]["summaryScore"]["value"]
                # if any category is above threshold (set to 0.9), flag it
                if not cleaned["flagged"] and response["attributeScores"][category]["summaryScore"]["value"] > threshold:
                    cleaned["flagged"] = True
            return asPercentages(cleaned)
            # return cleaned
        else:
            return response["attributeScores"]


def asPercentages(data):
    # Iterate over the dictionary and update the values
    for key, value in data.items():
        percentage = '{:.1%}'.format(value)
        data[key] = percentage
    return data


if __name__ == "__main__":
    m = PerspectiveClassifier()
    # pprint(m.evaluateText("I think you're ugly"))
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
        pprint(m.evaluateText(text))

# Perspective’s main attribute is TOXICITY, defined as “a rude, disrespectful, or unreasonable comment that is likely to make you leave a discussion”.
# For social science researchers using Perspective to study harassment, we recommend experimenting with thresholds of 0.7 or 0.9, similar to typical moderation use cases.
# For longer comments, the API can return a score for each individual sentence of the comment sent with the request. This can help moderators to identify the specific part of a longer comment that contains toxicity. This score is only available for some attributes. The summary score is the overall score for a particular attribute for the entire comment.
