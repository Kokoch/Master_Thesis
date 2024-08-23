from framework import *
class CLI():

    # Initialises the CLI class by creating an instance of the Framework class
    def __init__(self):
        self.framework = Framework()

    def run(self):
        # Main method to run the CLI. It sequentially calls methods to load datasets, set metrics, evaluate them, and report results
        self.__load_datasets_from_yaml()
        datasets = self.__add_dataset()
        if not datasets:
            print("No dataset(s) to be evaluated.")
            exit()
        else:
            self.__load_input_metrics_from_yaml()
            metrics = self.__set_metrics()
            if not metrics:
                print("No metrics to evaluate the dataset(s).")
                exit()
            else:
                data = self.__evaluate_metric()
                path = self.__create_csv_from_metrics(data)
                print("\nNow proceeding to the reporting of the results.")
                self.__reporting(data, path)

    # Method for reporting the results. It asks the user for the number of top datasets to show and displays the report
    def __reporting(self, data, csv_file):
        try:
            n = int(input("Show the top n datasets with n integer: n = "))
            self.framework.report(n,csv_file, data, )
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid integer.")
            self.__reporting(data, csv_file)  

    # Method to create a CSV file from the evaluated metrics. The user is asked whether they want to export the results 
    def __create_csv_from_metrics(self,data):
        create_csv = input('Would you like to export the results in a csv file ? (y/n)  --->  ').lower()
        if create_csv == "y":
            csv_file = str(input('\nPlease input the path and name of the csv file (e.g. ./output.csv): '))
            self.framework.create_csv_from_metrics(csv_file,data)
            return csv_file
        elif create_csv == "n":
            return None
        else:
            print("Invalid input, please try again.\n")
            self.__create_csv_from_metrics(data)  # Call the method again if input is invalid.

    # Method to evaluate the metrics against the loaded datasets
    def __evaluate_metric(self):
        print("\nNow proceeding to the evaluation of the metrics set for the loaded datasets.")
        data = self.framework.evaluate_metrics()
        return data    

    # Method to load input metrics from a YAML file. The user is asked if they want to load metrics from a file       
    def __load_input_metrics_from_yaml(self):
        metrics_from_yaml = input('\nWould you like to import metrics from yaml file ? (y/n)  --->  ').lower()
        if metrics_from_yaml == "y":
            yaml_file = str(input('\nPlease input the path to the yaml file: '))
            self.framework.metrics_eval = self.framework.metrics.load_input_metrics_from_yaml(yaml_file)
            if self.framework.metrics_eval:
                return self.framework.metrics_eval
            else: 
                self.__load_input_metrics_from_yaml() # If loading fails, prompt the user again
        elif metrics_from_yaml == "n":
            return self.framework.metrics_eval
        else:
            print("Invalid input, please try again.\n")
            self.__load_input_metrics_from_yaml() # Call the method again if input is invalid

    # Method to set the metrics manually. The user is asked if they want to set metrics manually or skip
    def __set_metrics(self):
        set_metric = input('Would you like to set the metrics manually? (y/n)  --->  ').lower()
        if set_metric == "y":
            metrics_info = {
                "Timeframe": "Enter the desired timeframe (e.g. 2018, 2019): ",
                "Revisit-Time": "Enter the maximum acceptable revisit time in days (integer): ",
                "Location": "Enter the required locations (e.g. USA, Canada): ",
                "Pixel-Scaling": "Enter the desired pixel scaling (low, medium, high): ",
                "Minimum-Image-Coverage": "Enter the minimum image coverage (integer): ",
                "NDVI": "Does the dataset need to support NDVI? (true/false): ",
                "Area": "Does the dataset need to support area calculations? (true/false): ",
                "Spectral-Bands": "Enter the required spectral bands (e.g. Red, Blue, NIR, Green): ",
                "Minimum-Number-of-Images": "Enter the minimum number of images (integer): ",
                "Image-Dimension": "Enter the required image dimensions (e.g. 256x256): "
            }
            print("\nPlease enter the following details for the metrics (press 'Enter' to skip any metric)")
            for metric_name, prompt in metrics_info.items():
                need = input(prompt).lower()
                if need:
                    self.framework.metrics_eval = self.framework.set_metric(metric_name, need)
                else:
                    continue
            return self.framework.metrics_eval   
        elif set_metric == "n":
            return self.framework.metrics_eval
        else:
            print("Invalid input, please try again.\n")
            self.__set_metrics() # Call the method again if input is invalid

    # Method to load datasets from a YAML file. The user is asked if they want to load datasets from a file.
    def __load_datasets_from_yaml(self):
        dataset_from_yaml = input('\nWould you like to import datasets from yaml file ? (y/n)  --->  ').lower()
        if dataset_from_yaml == "y":
            yaml_file = str(input('\nPlease input the path to the yaml file: '))
            self.framework.datasets_dict = self.framework.datasets.load_datasets_from_yaml(yaml_file)
            if self.framework.datasets_dict:
                return self.framework.datasets_dict
            else: 
                self.__load_datasets_from_yaml() # If loading fails, prompt the user again
        elif dataset_from_yaml == "n":
            return self.framework.datasets_dict
        else:
            print("Invalid input, please try again.\n")
            self.__load_datasets_from_yaml()

    # Method to add datasets manually. The user is asked if they want to add datasets manually.
    def __add_dataset(self):
        add_dataset = input('Would you like to add a dataset manually? (y/n)  --->  ').lower()
        while True:
            if add_dataset == "y":
                dataset_info = {
                    "ClassName": "Enter the class names separated by commas (e.g. class1, class2): ",
                    "CoverYear": "Enter the cover years separated by commas (e.g. 2020, 2021): ",
                    "Instrument": "Enter the instrument name (e.g. Sentinel-1, Sentinel-2): ",
                    "Localisation": "Enter the localisation details (e.g. France, Luxembourg): ",
                    "Name": "Enter the dataset name (e.g. Eurosat_RGB): ",
                    "Nb_Bands": "Enter the number of bands (integer): ",
                    "NbClass": "Enter the number of classes (integer): ",
                    "NbImage": "Enter the number of images (integer): ",
                    "PixelSize": "Enter the pixel size (e.g. 64x64, 128x128): ",
                    "Reference": "Enter the reference or link to the dataset: ",
                    "Spatial_Resolution_m": "Enter the spatial resolution in meters (e.g., 2, 10): ",
                    "Spectral_Resolution": "Enter the spectral bands (e.g. band1, band2): ",
                    "Use": "Enter the intended use of the dataset (e.g. Land Cover): ",
                    "ImageCoverage": "Enter the image coverage (float): ",
                    "Point_Cloud": "Enter if 3D Point Cloud is available (true/false): ",
                    "Open_Availability": "Enter the availability status (free/restrict): ",
                    "Revisit_Time": "Enter the revisit time (integer): ",
                    "ForestLabel": "Enter if forest labels are available (true/false): "
                }
                collected_data = {}
                print("\nPlease enter the following details for the dataset (press 'Enter' to skip any detail)")
                for key, prompt in dataset_info.items():
                    response = input(prompt)
                    if key in ["Nb_Bands", "NbClass", "NbImage", "Revisit_Time"]:
                        collected_data[key] = int(response) if response.isdigit() else 0
                    elif key in ["ImageCoverage", "Spatial_Resolution_m"]:
                        collected_data[key] = float(response) if response.replace('.', '', 1).isdigit() else 0.0
                    elif key in ["Point_Cloud", "ForestLabel"]:
                        collected_data[key] = response.lower() if response.lower() == 'true' else 'false'
                    else:
                        collected_data[key] = response if response else ""
                # Add the dataset to the framework
                self.framework.datasets_dict = self.framework.datasets.add_dataset(**collected_data)
                continue_adding = input('\nWould you like to add another dataset? (y/n)  --->  ').lower()
                while continue_adding != 'y':
                    if continue_adding == 'n':
                        return self.framework.datasets_dict
                    else:
                        print("Invalid input, please try again.\n")
                        continue_adding = input('\nWould you like to add another dataset? (y/n)  --->  ').lower()
            elif add_dataset == "n":
                return self.framework.datasets_dict
            else:
                print("Invalid input, please try again.\n")
                add_dataset = input('\nWould you like to add a dataset manually? (y/n)  --->  ').lower()
