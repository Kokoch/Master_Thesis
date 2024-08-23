import yaml
from tqdm import tqdm
import time


class Datasets:
    # Initialises the Datasets class with an empty dictionary to store datasets
    def __init__(self):
        self.datasets = {}

    # Displays a progress bar using tqdm for a specified duration to simulate processing time
    def progress_bar(self, duration):
        number_of_steps = 10
        for _ in tqdm(range(number_of_steps), desc="Processing"):
            time.sleep(duration / number_of_steps)

    # Loads datasets from a YAML file into the datasets dictionary
    def load_datasets_from_yaml(self, yaml_file):
        print("Loading datasets...")
        self.progress_bar(2) # Simulate loading time with a progress bar
        try:
            with open(yaml_file, 'r', encoding='utf-8') as file:
                datasets_yaml = yaml.safe_load(file)
                # Loop through each dataset in the YAML file
                for dataset in datasets_yaml['datasets']:
                    # Only add the dataset if it doesn't already exist to avoid overwriting.
                    if dataset['Name'] not in self.datasets:  
                        self.datasets[dataset['Name']] = dataset
                    else:
                        print(f"Dataset '{dataset['Name']}' already exists and was not overwritten.")
            print('Datasets loaded\n')
            return self.datasets

        # Handles the case where the YAML file is not found
        except FileNotFoundError:
            print(f"Error: The file {yaml_file} was not found.")
            return self.datasets
        # Handles errors that occur while parsing the YAML file
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return self.datasets
        # Handles any other exceptions that may occur
        except Exception as e:
            print(f"An error occurred: {e}")
            return self.datasets

    # Adds a new dataset to the datasets dictionary with the provided attributes
    def add_dataset(self,ClassName="",CoverYear="",Instrument="",Localisation="",Name="",Nb_Bands=0,NbClass=0,NbImage=0,PixelSize="",Reference="",Spatial_Resolution_m= 0,Spectral_Resolution= "",Use="", ImageCoverage = 0, Point_Cloud= "false",Open_Availability= "Free",Revisit_Time = 0, ForestLabel= "false"):
        dataset = {'ClassName': ClassName,'CoverYear': CoverYear,'Instrument': Instrument,'Localisation': Localisation,'Name': Name,'Nb Bands': Nb_Bands,'NbClass': NbClass,'NbImage': NbImage,'PixelSize': PixelSize,'Reference': Reference,'Spatial Resolution (m)': Spatial_Resolution_m,'Spectral Resolution': Spectral_Resolution,'Use': Use, 'ImageCoverage':ImageCoverage,'3DPoint': Point_Cloud,'Open-Availability': Open_Availability,'Revisit-Time': Revisit_Time, 'ForestLabel': ForestLabel}
        # Checks if a dataset with the same name already exists in the datasets dictionary
        if Name in self.datasets:
            print(f"Dataset with the name '{Name}' already exists.")
        else:
            # Adds the dataset to the dictionary if it doesn't already exist
            self.datasets[Name] = dataset
            print(f"Dataset '{Name}' added successfully.")
        return self.datasets
