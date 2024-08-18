import yaml
from tqdm import tqdm
import time

class Metrics:
    def __init__(self):
        self.metric_functions = {
            "Minimum-Number-of-Images": self.evaluate_minimum_number_of_images,
            "Minimum-Image-Coverage": self.evaluate_minimum_image_coverage,
            "Spectral-Bands": self.evaluate_spectral_bands,
            "Image-Dimension": self.evaluate_image_dimension,
            "Timeframe": self.evaluate_timeframe,
            "Pixel-Scaling": self.evaluate_pixel_scaling,
            "Area": self.evaluate_area,
            "NDVI": self.evaluate_ndvi,
            "Revisit-Time": self.evaluate_revisit_time,
            "Location": self.evaluate_location,
            "Open-Availability": self.evaluate_open_availability,
            "Usage-Defined": self.evaluate_usage_defined,
            "Metadata-Completeness": self.evaluate_metadata_completeness,
        }
        self.metrics_eval = []

    def add_metric(self, metric_name:str,eval_func):
        self.metric_functions[metric_name]=eval_func
        print(f"New metric '{metric_name}' added.\n")
        return self.metric_functions


    def set_metric(self,metric_name,need):
        for key in self.metric_functions:
            if metric_name.lower() == key.lower():
                for metric in self.metrics_eval:
                    if metric[0].lower() == metric_name.lower():
                        metric[1] = str(need)
                        print(f"Metric '{metric_name}' set with need: '{need}'.\n")
                        return self.metrics_eval
                self.metrics_eval.append([key,str(need)])
                print(f"Metric '{metric_name}' set with need: '{need}'.\n")
                return self.metrics_eval      
            else:
                continue
        print('No metric set because your metric doesn\'t exist\n')            
        return self.metrics_eval


    def progress_bar(self, duration):
        number_of_steps = 10
        for _ in tqdm(range(number_of_steps), desc="Processing"):
            time.sleep(duration / number_of_steps)

    def load_input_metrics_from_yaml(self, yaml_file):
        try:
            with open(yaml_file, 'r') as file:
                content = yaml.safe_load(file)
                self.input_metrics = {metric['name']: metric['need'] for metric in content['metrics'] if metric.get('need')}

            print("Importing the input metrics...")
            self.progress_bar(1)
            print('Input metrics loaded\n')
            
            print("Checking correctness of input metrics...")
            self.progress_bar(1)
            print("Metrics checked to retain only those that can be evaluated\n")
            return self.check_input_metrics()
        
        except FileNotFoundError:
            print(f"Error: The file {yaml_file} was not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_input_metrics(self):
        for metric, need in self.input_metrics.items():
            if metric in self.metric_functions:
                found = False
                for metric_eval in self.metrics_eval:
                    if metric == metric_eval[0]:
                        metric_eval[1] = need
                        found = True
                if not found:
                    self.metrics_eval.append([metric, need])
        return self.metrics_eval

    def evaluate_timeframe(self, need, datasets:dict):
        output = []
        needed_years = set(map(int, need.replace(" ", "").split(',')))
        for dataset_name, dataset in datasets.items():
            dataset_years = set(map(int, dataset.get("CoverYear", "").replace(" ", "").split(','))) if dataset.get("CoverYear", "") else set()
            covered_years = needed_years & dataset_years
            satisfaction_percentage = (len(covered_years) / len(needed_years)) * 100 if needed_years else 0
            output.append([dataset_name, int(satisfaction_percentage)])
        return output

    def evaluate_revisit_time(self, need, datasets:dict):
        output = []
        for dataset_name, dataset in datasets.items():
            dataset_revisit_time = float(dataset.get("Revisit-Time", 0))
            score = int(min((float(need) / dataset_revisit_time) * 100,100) if dataset_revisit_time > 0 else 0)
            output.append([dataset_name, score])
        return output

    def evaluate_location(self, need, datasets:dict):
        output = []
        needed_locations = set(need.lower().replace(", ", ",").split(","))
        for dataset_name, dataset in datasets.items():
            dataset_locations = set(dataset.get("Localisation", "").lower().replace(", ", ",").split(","))
            score = int((len(needed_locations & dataset_locations) / len(needed_locations)) * 100 if needed_locations else 0)
            output.append([dataset_name, score])
        return output

    def evaluate_pixel_scaling(self, need, datasets:dict):
        output = []
        thresholds = {'low': 30, 'medium': (5, 30), 'high': 5}
        need_list = need.lower().replace(" ", "").split(",")

        for dataset_name, dataset in datasets.items():
            spatial_resolutions = list(map(float, str(dataset.get("Spatial Resolution (m)", "0")).replace(" ", "").split(",")))
            scores = [self.calculate_pixel_scaling_score(need, thresholds, spatial_resolutions) for need in need_list]
            avg_score = int(sum(scores) / len(scores)) if scores else 0
            output.append([dataset_name, avg_score])
        return output

    def calculate_pixel_scaling_score(self, need, thresholds, spatial_resolutions):
        score = 0
        for resolution in spatial_resolutions:
            if (need == 'low' and resolution >= thresholds['low']) or \
               (need == 'medium' and thresholds['medium'][0] < resolution < thresholds['medium'][1]) or \
               (need == 'high' and resolution <= thresholds['high']):
                score = 100
                break
        return score

    def evaluate_minimum_image_coverage(self, need, datasets:dict):
        output = []
        for dataset_name, dataset in datasets.items():
            image_coverage = int(dataset.get("ImageCoverage", 0))
            score = 100 if image_coverage >= int(need) else int((image_coverage / int(need)) * 100)
            output.append([dataset_name, score])
        return output

    def evaluate_spectral_bands(self, need, datasets:dict):
        output = []
        needed_bands = set(need.lower().replace(", ", ",").split(","))
        for dataset_name, dataset in datasets.items():
            dataset_bands = set(dataset.get("Spectral Resolution", "").lower().replace(", ", ",").split(","))
            score = int((len(needed_bands & dataset_bands) / len(needed_bands)) * 100 if needed_bands else 0)
            output.append([dataset_name, score])
        return output

    def evaluate_image_dimension(self, need, datasets:dict):
        output = []
        needed_dimensions = [tuple(map(int, n.replace(" ", "").split('x'))) if 'x' in n else (int(n.replace(" ", "")), int(n.replace(" ", ""))) for n in need.split(',')]
        for dataset_name, dataset in datasets.items():
            pixel_sizes = [tuple(map(int, ps.split('x'))) if 'x' in ps else (int(ps), int(ps)) for ps in dataset.get("PixelSize", "").replace(" ", "").split(',') if ps]
            scores = [self.calculate_dimension_score(dim, needed_dimensions) for dim in pixel_sizes]
            avg_score = int(sum(scores) / len(scores)) if scores else 0
            output.append([dataset_name, avg_score])
        return output

    def calculate_dimension_score(self, dimension, needed_dimensions):
        width, height = dimension
        for needed_width, needed_height in needed_dimensions:
            if width >= needed_width and height >= needed_height and width % needed_width == 0 and height % needed_height == 0:
                return 100
        return 0

    def evaluate_minimum_number_of_images(self, need, datasets:dict):
        output = []
        for dataset_name, dataset in datasets.items():
            nb_images = int(dataset.get("NbImage", 0))
            score = 100 if nb_images >= int(need) else int((nb_images / int(need)) * 100)
            output.append([dataset_name, score])
        return output

    def evaluate_open_availability(self, datasets:dict):
        output = []
        for dataset_name, dataset in datasets.items():
            score = 100 if dataset.get("Open-Availability", "").lower() == "free" else 0
            output.append([dataset_name, score])
        return output

    def evaluate_usage_defined(self, datasets:dict):
        output = []
        for dataset_name, dataset in datasets.items():
            score = 100 if dataset.get("Use", "") else 0
            output.append([dataset_name, score])
        return output

    def evaluate_metadata_completeness(self, datasets:dict):
        required_fields = ["Use", "CoverYear", "Localisation", "Revisit-Time", "ImageCoverage", "NbImage", "Spatial Resolution (m)", "Spectral Resolution", "PixelSize", "Open-Availability"]
        output = []
        for dataset_name, dataset in datasets.items():
            total_fields = len(required_fields)
            available_fields = sum(1 for field in required_fields if dataset.get(field, "") != "" and dataset.get(field, 0) != 0)
            score = (available_fields / total_fields) * 100
            output.append([dataset_name, int(score)])
        return output

    def evaluate_ndvi(self, datasets:dict):
        output = []
        ndvi_relevant_bands = "Red, NIR"
        spectral_band_results = self.evaluate_spectral_bands(ndvi_relevant_bands, datasets)
        for result in spectral_band_results:
            dataset_name, spectral_score = result
            ndvi_score = 100 if spectral_score == 100 else 0
            output.append([dataset_name, ndvi_score])
        return output
    
    def evaluate_point_cloud_data(self,datasets:dict):
        output = []
        for dataset_name, dataset in datasets.items():
            cloud_point = str(dataset.get("3dPointCloud", "")).replace(" ", "").lower()
            dataset_name = dataset.get("Name",0)
            if cloud_point == "true":
                score = 100
            else:
                score = 0
            output.append([dataset_name, int(score)])
        return output

    def evaluate_forest_label(self,datasets:dict):
        output = []
        for dataset_name, dataset in datasets.items():
            forest_label = str(dataset.get("ForestLabel", "")).replace(" ", "").lower()
            dataset_name = dataset.get("Name",0)
            if forest_label == "true":
                score = 100
            else:
                score = 0
            output.append([dataset_name, int(score)])
        return output

    def evaluate_area(self, datasets:dict):
        output = []
        high_resolution_results = self.evaluate_pixel_scaling('High', datasets)
        low_medium_high_resolution_results = self.evaluate_pixel_scaling('Low, Medium, high', datasets)
        rgb_results = self.evaluate_spectral_bands('Red, Blue, Green', datasets)
        ndvi_results = self.evaluate_spectral_bands('Red, NIR', datasets)
        lidar_results = self.evaluate_point_cloud_data(datasets)
        forest_label_results = self.evaluate_forest_label(datasets)
        dataset_names = set([result[0] for result in high_resolution_results + low_medium_high_resolution_results + 
                            rgb_results + ndvi_results + lidar_results + forest_label_results])
        for dataset_name in dataset_names:
            dataset_score = {
                'high_resolution': next((item[1] for item in high_resolution_results if item[0] == dataset_name), 0),
                'low_medium_high_resolution': next((item[1] for item in low_medium_high_resolution_results if item[0] == dataset_name), 0),
                'rgb': next((item[1] for item in rgb_results if item[0] == dataset_name), 0),
                'ndvi': next((item[1] for item in ndvi_results if item[0] == dataset_name), 0),
                'lidar': next((item[1] for item in lidar_results if item[0] == dataset_name), 0),
                'forest_label': next((item[1] for item in forest_label_results if item[0] == dataset_name), 0)
            }
            if dataset_score['high_resolution'] == 100 and dataset_score['lidar'] == 100:
                final_score = 100
            elif dataset_score['low_medium_high_resolution'] > 0:
                if dataset_score['ndvi'] == 100:
                    final_score = 100
                elif dataset_score['rgb'] == 100 and dataset_score['ndvi'] != 100:
                    if dataset_score['forest_label'] == 100:
                        final_score = 100
                    else: 
                        final_score = 0
                else:
                    final_score = 0
            else: 
                final_score = 0
            output.append([dataset_name, final_score])
        return output

