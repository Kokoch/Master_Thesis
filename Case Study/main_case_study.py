from framework import *

def evaluate_label(need: str, datasets: dict) -> list:
    output = []
    # Convert the input labels string to a list of labels
    input_labels_list = need.lower().replace(", ", ",").split(",")

    # Iterate over each dataset in the datasets dictionary
    for dataset_name, dataset in datasets.items():
        matching_labels = 0  # Counter for matching labels

        # Convert the dataset's 'ClassName' string to a list of labels
        dataset_labels_list = dataset.get("ClassName", "").lower().replace(", ", ",").split(",")
    
        # Check for each label in input_labels_list if it exists in dataset_labels_list
        for label in input_labels_list:
            if label in dataset_labels_list:
                # Increment the counter if there is a match
                matching_labels += 1  

        # Calculate the satisfaction percentage
        result = int(matching_labels / len(input_labels_list) * 100)

        # Append the dataset name and its satisfaction percentage to the output list
        output.append([dataset_name, result])
    return output


if __name__ == "__main__":
    # Create an instance of the Framework class
    framework = Framework()

    # Load datasets from a YAML file
    framework.load_datasets_from_yaml('./datasets.yaml')

    # Add a custom metric called 'Label' using the evaluate_label function
    framework.add_metric('Label', evaluate_label)

    # Load input metrics from another YAML file
    framework.load_input_metrics_from_yaml('./metrics.yaml')

    # Evaluate the loaded datasets against the loaded metrics
    data = framework.evaluate_metrics()

    # Create a CSV file from the evaluation results and save it as 'output.csv'
    framework.create_csv_from_metrics('./output.csv',data)

    # Generate a report showing the top 3 datasets based on the evaluation and save the report to 'output.csv'
    output = framework.report(3,'./output.csv',data)
