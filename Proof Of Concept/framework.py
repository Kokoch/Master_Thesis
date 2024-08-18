import time
import pandas as pd
import csv
from tqdm import tqdm
from metrics import *
from datasets import *
import os

class Framework:
    def __init__(self):
        self.metrics = Metrics()
        self.datasets = Datasets()
        self.metrics_eval = []
        self.datasets_dict = {}
        self.results = []

    def progress_bar(self, duration):
        number_of_steps = 10
        for _ in tqdm(range(number_of_steps), desc="Processing"):
            time.sleep(duration / number_of_steps)

    def set_metric(self,metric_name:str,need):
        self.metrics_eval = self.metrics.set_metric(metric_name,need)
        return self.metrics_eval
    
    def add_metric(self,metric_name:str, eval_func):
        return self.metrics.add_metric(metric_name,eval_func)
    
    def add_dataset(self,Name,ClassName="",CoverYear="",Instrument="",Localisation="",Nb_Bands=0,NbClass=0,NbImage=0,PixelSize="",Reference="",Spatial_Resolution_m= 0,Spectral_Resolution= "",Use="", ImageCoverage = 0, Point_Cloud= "false",Open_Availability= "Free",Revisit_Time = 0, ForestLabel= "false"):
        self.datasets_dict = self.datasets.add_dataset(ClassName,CoverYear,Instrument,Localisation,Name,Nb_Bands,NbClass,NbImage,PixelSize,Reference,Spatial_Resolution_m,Spectral_Resolution,Use, ImageCoverage, Point_Cloud,Open_Availability,Revisit_Time, ForestLabel)
        return self.datasets_dict

    def load_input_metrics_from_yaml(self, yaml_file):
        self.metrics_eval = self.metrics.load_input_metrics_from_yaml(yaml_file) 
        return self.metrics_eval
    
    def load_datasets_from_yaml(self, yaml_file):
        self.datasets_dict = self.datasets.load_datasets_from_yaml(yaml_file)
        return self.datasets_dict

    def evaluate_metrics(self):
        results = []
        if self.metrics_eval and self.datasets_dict:
            for metric_name, metric_value in self.metrics_eval:
                if metric_name in ["Area", "NDVI"] and str(metric_value).lower() == "true":
                    function = self.metrics.metric_functions.get(metric_name)
                    if function:
                        output = function(self.datasets_dict)
                        results.append([metric_name, output])
                else:
                    function = self.metrics.metric_functions.get(metric_name)
                    if function:
                        output = function(metric_value, self.datasets_dict)
                        results.append([metric_name, output])

            results.append(["Open-Availability",self.metrics.evaluate_open_availability(self.datasets_dict)])
            results.append(["Usage-Defined",self.metrics.evaluate_usage_defined(self.datasets_dict)])
            results.append(["Metadata-Completeness",self.metrics.evaluate_metadata_completeness(self.datasets_dict)])

            print("Evaluating the satisfaction percentage for each input metric...")
            self.progress_bar(max(len(self.metrics_eval), 2))
            print("Evaluation completed\n")
            self.results = results
            return results
        else:
            print("No metrics set or datasets to evaluate")
            return self.results

    def create_csv_from_metrics(self,output_file='./temp_csv.csv', data = None):
        if data is None:
            data = self.results
        if data:
            results_dict = {}
            for metric, dataset_scores in data:
                for dataset_name, score in dataset_scores:
                    if dataset_name not in results_dict:
                        results_dict[dataset_name] = {}
                    results_dict[dataset_name][metric] = score

            metrics = [metric for metric, _ in data]
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Dataset Name'] + metrics)
                for dataset_name, scores in results_dict.items():
                    row = [dataset_name] + [scores.get(metric, '') for metric in metrics]
                    writer.writerow(row)
        else:
            print("No CSV file to create ")

    def report(self, n:int = 5, csv_file=None, data=None):
        try: 
            if csv_file is None:
                self.create_csv_from_metrics(data=data) 
                csv_temp = './temp_csv.csv'
            else: 
                csv_temp = csv_file

            data = pd.read_csv(csv_temp)
            excluded_columns = ['Open-Availability', 'Usage-Defined', 'Metadata-Completeness']
            data['Average Satisfaction'] = data.drop(columns=['Dataset Name'] + excluded_columns).mean(axis=1).round(3)
            sorted_data = data.sort_values(by=['Average Satisfaction', 'Metadata-Completeness'], ascending=[False, False]).reset_index(drop=True)
            sorted_data['Rank'] = sorted_data.index + 1
            sorted_data.to_csv(csv_temp, index=False)

            if n > len(sorted_data):
                n = len(sorted_data) - 1
                
            print(f"Top '{n}' datasets:")
            for index, row in sorted_data.iterrows():
                print(f"{row['Rank']}: {row['Dataset Name']} - Avg. Satisfaction: {row['Average Satisfaction']:.2f}%,\n           Usage-Defined: {row['Usage-Defined']}%,\n           Open-Availability: {row['Open-Availability']}%,\n           Metadata-Completeness: {row['Metadata-Completeness']}%\n")
                if index == n-1:
                    break

            top_datasets = sorted_data.head(n)
            output = [row.to_dict() for _, row in top_datasets.iterrows()]

            if csv_file is None and os.path.exists(csv_temp):
                os.remove('./temp_csv.csv')
            return output
        except:
            print("No evaluation was made")
            

