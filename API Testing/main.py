from pprint import pprint
from perspective import PerspectiveClassifier
from openAI import OpenAIClassifier
import csv

DATA_FOLDER = "../Datasets/"


def readCSV(filename, numRows=10):
    returnData = []
    with open(DATA_FOLDER + filename, 'r') as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)
        count = 0

        # Read the data row by row
        for row in reader:
            returnData.append({
                "text": row['tweet_text'],
                "is_cyberbullying": row['cyberbullying_type'] != "not_cyberbullying"
            })

            count += 1
            if count > numRows:
                return returnData


if __name__ == "__main__":
    models = {"perspective": PerspectiveClassifier(),
              "openAI": OpenAIClassifier()}

    csvData = readCSV('cyberbullying_tweets.csv', numRows=10000)

    for kvp in csvData:
        content = kvp["text"]
        isReallyCyberbullying = kvp["is_cyberbullying"]

        if isReallyCyberbullying:
            print(
                f'------------------------------ String: {content} ------------------------------')

            for label, model in models.items():
                scores = model.evaluateText(content)
                pprint(scores)
                print()

        # print(
        #     f'------------------------------ String: {content} ------------------------------')
        # for label, model in models.items():
        #     print(f'================== Classifier: {label} =================')
        #     pprint(scores)
        #     print()
        # print(
        #     f'------------------------------ Actual: {trueValue} ------------------------------\n\n\n')
