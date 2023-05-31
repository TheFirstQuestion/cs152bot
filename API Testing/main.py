from pprint import pprint
from perspective import PerspectiveClassifier
from openAI import OpenAIClassifier

testing_data = ["I think you're ugly", "u r fat",
                "i think you stink", "screw you", "oh shit"]

if __name__ == "__main__":
    models = {"perspective": PerspectiveClassifier(),
              "openAI": OpenAIClassifier()}

    for str in testing_data:
        print(f'String: {str}')
        for label, model in models.items():
            print(f'Classifier: {label}')
            pprint(model.evaluateText(str))
            print()
        print("==================")
