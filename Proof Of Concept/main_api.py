from framework import *

if __name__ == "__main__":
    # The Expert User initiates the session by invoking the Framework’s initialisation
    framework = Framework()

    # The Expert User issues a command to load datasets from a yaml file by calling
    framework.load_datasets_from_yaml('./datasets.yaml')

    # The Expert User sets the evaluation metric Location with specific requirement Luxembourg by using
    framework.set_metric("Location", "Luxembourg")

    # The Expert User triggers the evaluation process through the evaluate() method
    final_result = framework.evaluate_metrics()

    # The Expert User requests CSV file that contains the result of the evaluation using
    framework.create_csv_from_metrics('./ final_result.csv', final_result)

    # The Expert User requests a report of the top 5 datasets by executing
    output = framework.report(5,'./ final_result.csv')
