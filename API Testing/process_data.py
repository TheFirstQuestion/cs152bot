import csv
from pprint import pprint

DATA_FOLDER = "../Datasets/"
DATASETS = ['aggression_parsed_dataset.csv', 
            "attack_parsed_dataset.csv", 
            "kaggle_parsed_dataset.csv",
            "toxicity_parsed_dataset.csv",
            "twitter_parsed_dataset.csv",
            "twitter_racism_parsed_dataset.csv",
            "twitter_sexism_parsed_dataset.csv",
            "youtube_parsed_dataset.csv"]
# "cyberbullying_tweets.csv", 

def extract_csv(filenames):
    returnData = []
    for filename in filenames:
        with open(DATA_FOLDER + filename, 'r') as file, open(DATA_FOLDER + 'extracted_' + filename, 'w', newline="") as out:
        # Create a CSV reader object
            reader = csv.DictReader(file)
            count = 0
            fieldnames = ['Text', 'oh_label']
            writer = csv.DictWriter(out, fieldnames = fieldnames)
            writer.writeheader()
            # Read the data row by row
            for row in reader:
                if len(row['Text']) < 62: 
                    writer.writerow({'Text': row['Text'], 'oh_label': row['oh_label']})
                
# extract_csv(DATASETS)

def compile_toxic(filenames):
    with open(DATA_FOLDER + 'toxic.csv', 'w', newline="") as out:
        fieldnames = ['Text', 'oh_label']
        writer = csv.DictWriter(out, fieldnames = fieldnames)
        writer.writeheader()
        count = 0
        # parse through them
        for filename in filenames:
            with open(DATA_FOLDER + 'extracted_' + filename, 'r') as file:
            # Create a CSV reader object
                reader = csv.DictReader(file)
                # Read the data row by row
                for row in reader:
                    if row['oh_label'] != '0': 
                        print(row['Text'], row['oh_label'])
                        count += 1
                        writer.writerow({'Text': row['Text'], 'oh_label': row['oh_label']})
    print('count', count)

def filter_toxic(filenames):
    for filename in filenames:
            with open(DATA_FOLDER + 'extracted_' + filename, 'r') as file, open(DATA_FOLDER + 'toxic_' + filename, 'w', newline="") as out_toxic, open(DATA_FOLDER + 'non_toxic_' + filename, 'w', newline="") as out_non_toxic:
            # Create a CSV reader object
                reader = csv.DictReader(file)
                fieldnames = ['Text', 'oh_label']
                writer_toxic = csv.DictWriter(out_toxic, fieldnames = fieldnames)
                writer_toxic.writeheader()
                writer_non_toxic = csv.DictWriter(out_non_toxic, fieldnames = fieldnames)
                writer_non_toxic.writeheader()
                count = 0
                # Read the data row by row
                for row in reader:
                    count += 1
                    if row['oh_label'] != '0': 
                        writer_toxic.writerow({'Text': row['Text'], 'oh_label': row['oh_label']})
                    else:
                        writer_non_toxic.writerow({'Text': row['Text'], 'oh_label': row['oh_label']})
    print('count', count)

def compile_non_toxic(filenames):
    with open(DATA_FOLDER + 'non_toxic.csv', 'w', newline="") as out:
        fieldnames = ['Text', 'oh_label']
        writer = csv.DictWriter(out, fieldnames = fieldnames)
        writer.writeheader()
        count = 0
        # parse through them
        for filename in filenames:
            with open(DATA_FOLDER + 'extracted_' + filename, 'r') as file:
            # Create a CSV reader object
                reader = csv.DictReader(file)
                # Read the data row by row
                for row in reader:
                    if row['oh_label'] == '0': 
                        print(row['Text'], row['oh_label'])
                        count += 1
                        writer.writerow({'Text': row['Text'], 'oh_label': row['oh_label']})
                        
    print('count', count)
        
# extract_csv(DATASETS)
# compile_toxic(DATASETS)
# compile_non_toxic(DATASETS)
filter_toxic(DATASETS)

