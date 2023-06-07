from pprint import pprint
from perspective import PerspectiveClassifier
from openAI import OpenAIClassifier
import csv
from datetime import datetime
from tqdm import tqdm
from langdetect import detect


DATA_FOLDER = "../Datasets/"
OUTPUT_FOLDER = "Confusion_Matrix_Data/"


def readCSV(filename, maxRows=100):
    returnData = []
    with open(DATA_FOLDER + filename, 'r') as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)
        count = 0

        print(f"\nReading data for {filename}...")
        # Read the data row by row
        for row in tqdm(reader):
            text = row['Text']
            # Ensure good length
            if len(text) > 60 or len(text) < 3:
                pass
            # Skip if not English or can't detect language
            try:
                if detect(text) != "en":
                    pass
            except:
                pass

            returnData.append({
                "text": text,
                "ground_truth": row['oh_label'] == '1'
            })

            count += 1
            if count >= maxRows:
                return returnData

    return returnData


if __name__ == "__main__":
    # Merge the data into one dict
    rows = 10000
    data = readCSV('final_toxic.csv', maxRows=rows) + \
        readCSV('final_non_toxic.csv', maxRows=rows)

    # We'll use these in the filenames
    current_datetime = datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    models = {"openAI": OpenAIClassifier(),
              "perspective": PerspectiveClassifier()}

    # These are the categories rated by each model
    headers = {"openAI": ['violence/graphic',
                          'self-harm', 'hate/threatening', 'sexual/minors', 'hate', 'violence', 'sexual'],
               "perspective": ['threat', 'insult', 'identity_attack', 'flagged', 'severe_toxicity', 'profanity', 'toxicity', "sexually_explicit", "flirtation"]}

    print()
    print()

    for label, model in models.items():
        with open(f"{OUTPUT_FOLDER}{timestamp}_{label}.csv", 'x', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=["text", "ground_truth"] + headers[label])
            writer.writeheader()

            print(f"Evaluating data using {label}...")
            for kvp in tqdm(data):
                try:
                    result = model.evaluateText(kvp["text"])
                    writer.writerow({**kvp, **result})
                except:
                    # Just ignore it if there's an error
                    pass

# Run 2023-06-06_20-46-20 took 8m 35s
# Reading data for final_toxic.csv...
# 250it [00:02, 122.94it/s]
# Reading data for final_non_toxic.csv...
# 748it [00:04, 164.43it/s]
# Evaluating data using openAI...
# 100% = 998/998 [05:11<00:00,  3.20it/s]
# Evaluating data using perspective...
# 100% = 998/998 [03:13<00:00,  5.15it/s]
