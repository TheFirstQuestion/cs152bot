from pprint import pprint
from perspective import PerspectiveClassifier
from openAI import OpenAIClassifier
import csv
import time

DATA_FOLDER = "../Datasets/"
DATASETS = ['aggression_parsed_dataset.csv', 
            "kaggle_parsed_dataset.csv",
            "twitter_parsed_dataset.csv",
            "twitter_racism_parsed_dataset.csv",
            "twitter_sexism_parsed_dataset.csv",
            ]


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
                    "is_cyberbullying": row['oh_label'] == '1'
                })
            count += 1
            if count >= numRows:
                return returnData
        print("len(returnData)", len(returnData))
    return returnData
        
def classify(filename, numRows = 250):
    models = {"openAI": OpenAIClassifier(),
              "perspective": PerspectiveClassifier()}
    csvData = []
    csvData = readCSV(filename, numRows=numRows)
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
                text_class = ''
                # time buffer for rate limit
                time.sleep(1)
                if eval["flagged"] == True:
                    if isReallyCyberbullying:
                        TP += 1
                        text_class = 'TP'
                    else:
                        FP += 1
                        text_class = 'FP'
                elif eval["flagged"] == False:
                    if isReallyCyberbullying:
                        FN += 1
                        text_class = 'FN'
                    else:
                        TN += 1
                        text_class = 'TN'
                TOTAL += 1
                print(text_class, "Summary: TP,FP,TN,FN,TOTAL,ERRORs:", TP, FP, TN, FN, TOTAL, ERRORS, content)    
            except:
                time.sleep(1)
                print("error", content)
                print(text_class, "Summary: TP,FP,TN,FN,TOTAL,ERRORs:", TP, FP, TN, FN, TOTAL, ERRORS, content) 
                ERRORS += 1
                if ERRORS > 20:
                    break
        print('FINAL', label, "TP, FP, TN, FN, TOTAL, ERRORs", TP, FP, TN, FN, TOTAL, ERRORS)


if __name__ == "__main__":
    classify('final_toxic.csv')
    classify('final_non_toxic.csv', numRows = 750)
    