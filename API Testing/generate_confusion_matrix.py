import pandas as pd
from sklearn.metrics import confusion_matrix


OPENAI_PATH = "Confusion_Matrix_Data/2023-06-07_10-32-10_openAI.csv"
PERSPECTIVE_PATH = "Confusion_Matrix_Data/2023-06-06_20-46-20_perspective.csv"


if __name__ == "__main__":
    # Read the CSV file into a pandas DataFrame
    openAIData = pd.read_csv(OPENAI_PATH)

    # Extract the actual and predicted labels from the DataFrame
    openAI_actual_labels = openAIData['ground_truth']
    openAI_predicted_labels = openAIData['flagged']

    # Create the confusion matrix
    print("openAI")
    print(confusion_matrix(openAI_actual_labels, openAI_predicted_labels))

    print()

    # Read the CSV file into a pandas DataFrame
    perspectiveData = pd.read_csv(PERSPECTIVE_PATH)
    # Extract the actual and predicted labels from the DataFrame
    perspective_actual_labels = perspectiveData['ground_truth']

    for THRESHOLD_1 in range(75, 95, 2):
        for THRESHOLD_2 in range(THRESHOLD_1, 100, 2):
            perspective_predicted_labels = perspectiveData['toxicity'] >= (
                THRESHOLD_2 / 100)

            # Create the confusion matrix
            print(f"Perspective (t={THRESHOLD_2}) Auto-flag")
            print(confusion_matrix(perspective_actual_labels,
                                   perspective_predicted_labels))

            numMessages = len(perspectiveData)
            print(f'Total number of messages: {numMessages}')

            print(f"THRESHOLD_1 = {THRESHOLD_1}, THRESHOLD_2 = {THRESHOLD_2}")

            numAutoFlagged = (
                perspectiveData["toxicity"] >= (THRESHOLD_2/100)).sum()
            # print(f'Auto-flagged: {numAutoFlagged} ({int(numAutoFlagged / numMessages * 100)}%)')

            numManualReview = (perspectiveData["toxicity"] >= (
                THRESHOLD_1/100)).sum() - numAutoFlagged
            print(
                f'Manually Reviewed: {numManualReview} ({int(numManualReview / numMessages * 100)}%)')

            print()
