from pprint import pprint
from perspective import PerspectiveClassifier
from openAI import OpenAIClassifier
import csv
import time

DATA_FOLDER = "../Datasets/"
DATASETS = ['aggression_parsed_dataset.csv', 
            "attack_parsed_dataset.csv", 
            "cyberbullying_tweets.csv", 
            "kaggle_parsed_dataset.csv",
            "toxicity_parsed_dataset.csv",
            "twitter_parsed_dataset.csv",
            "twitter_racism_parsed_dataset.csv",
            "twitter_sexism_parsed_dataset.csv",
            "youtube_parsed_dataset.csv"]


def readCSV(filename, numRows=100):
    returnData = []
    with open(DATA_FOLDER + filename, 'r') as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)
        count = 0

        # Read the data row by row
        for row in reader:
            # print("reading row")
            if filename == "cyberbullying_tweets.csv":
                if len(row['tweet_text']) > 62:
                    pass
                returnData.append({
                    "text": row['tweet_text'],
                    "is_cyberbullying": row['cyberbullying_type'] != "not_cyberbullying"
                })
            # other datasets
            else:
                if len(row['Text']) > 60:
                    pass
                returnData.append({
                    "text": row['Text'],
                    "is_cyberbullying": row['oh_label'] == 1
                })
            count += 1
            if count > numRows:
                return returnData
        print("len(returnData)", len(returnData))
    return returnData
        

# if __name__ == "__main__":
#     models = {"perspective": PerspectiveClassifier(),
#               "openAI": OpenAIClassifier()}

#     csvData = readCSV('cyberbullying_tweets.csv', numRows=10000)

#     for kvp in csvData:
#         content = kvp["text"]
#         isReallyCyberbullying = kvp["is_cyberbullying"]

#         if isReallyCyberbullying:
#             print(
#                 f'------------------------------ String: {content} ------------------------------')

#             for label, model in models.items():
#                 try:
#                     scores = model.evaluateText(content)
#                     pprint(scores)
#                     print()
#                 except:
#                     print(f"an error occurred skipping {content}")
# 
if __name__ == "__main__":
    models = {"perspective": PerspectiveClassifier(),
              "openAI": OpenAIClassifier()}
    
    
    
    for dataset in DATASETS:
        csvData = []
        csvData = readCSV('cyberbullying_tweets.csv', numRows=10000)
        print("len(csvData)", len(csvData))

        for label, model in models.items():
            print(label)
            TP = 0
            TN = 0
            FP = 0
            FN = 0
            TOTAL = 0
            ERRORS = 0
            for kvp in csvData:
                content = kvp["text"]
                isReallyCyberbullying = kvp["is_cyberbullying"]
                try:
                    eval = model.evaluateText(content)
                    # time buffer for rate limit
                    time.sleep(1)
                    if eval["flagged"] == True:
                        if isReallyCyberbullying:
                            TP += 1
                        else:
                            FP += 1
                    elif eval["flagged"] == False:
                        if isReallyCyberbullying:
                            FN += 1
                        else:
                            TN += 1
                    TOTAL += 1    
                except:
                    print("error", content)
                    ERRORS += 1
                    if ERRORS > 20:
                        break
            print(label, "TP, FP, TN, FN, TOTAL, ERRORs", TP, FP, TN, FN, TOTAL, ERRORS)
            

        

    

            


        # print(
        #     f'------------------------------ String: {content} ------------------------------')
        # for label, model in models.items():
        #     print(f'================== Classifier: {label} =================')
        #     pprint(scores)
        #     print()
        # print(
        #     f'------------------------------ Actual: {trueValue} ------------------------------\n\n\n')
