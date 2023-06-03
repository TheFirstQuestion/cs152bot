import csv

# Open the CSV file
with open('cyberbullying_tweets.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.DictReader(file)

    # Read the data row by row
    for row in reader:
        # Access the values of each column using the headers
        column1_value = row['tweet_text']
        column2_value = row['cyberbullying_type']

        # Process the data as needed
        # Example: print the values of the first two columns
        print(f'{column1_value} ===> {column2_value}')
        break
