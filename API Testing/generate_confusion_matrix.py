import pandas as pd
from sklearn.metrics import confusion_matrix


DATASET_PATH = "Confusion_Matrix_Data/2023-06-07_10-32-10_openAI.csv"


if __name__ == "__main__":
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(DATASET_PATH)

    # Extract the actual and predicted labels from the DataFrame
    actual_labels = data['ground_truth']
    predicted_labels = data['flagged']

    # Create the confusion matrix
    cm = confusion_matrix(actual_labels, predicted_labels)

    # Print the confusion matrix
    print(cm)
