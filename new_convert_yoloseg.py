import os
import json
import random
import string
from datetime import datetime

def convert_yolo_to_ls(yolo_coords, original_width, original_height):
    def convert_x(x): return x * 100.0 
    def convert_y(y): return y * 100.0 

    points = []
    for i in range(0, len(yolo_coords), 2):
        x = convert_x(yolo_coords[i])
        y = convert_y(yolo_coords[i+1])
        points.append([x, y])

    return points

def generate_unique_id(existing_ids, length=10):
    while True:
        new_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            return new_id

def process_yolo_file(file_path, image_dimensions, existing_ids, class_names):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if not lines:
        return []

    original_width = image_dimensions["original_width"]
    original_height = image_dimensions["original_height"]

    results = []
    current_label = None
    yolo_coords = []

    for line in lines:
        data = line.split()
        if data[0].isdigit():
            # Save the previous annotation if it exists
            if current_label is not None and yolo_coords:
                points = convert_yolo_to_ls(yolo_coords, original_width, original_height)
                polygon_label = class_names[current_label]
                unique_id = generate_unique_id(existing_ids)

                result = {
                    "original_width": original_width,
                    "original_height": original_height,
                    "image_rotation": 0,
                    "value": {
                        "points": points,
                        "closed": True,
                        "polygonlabels": [polygon_label]
                    },
                    "id": unique_id,
                    "from_name": "label",
                    "to_name": "image",
                    "type": "polygonlabels",
                    "origin": "manual"
                }

                results.append(result)
                yolo_coords = []

            current_label = int(data[0])
            yolo_coords.extend(map(float, data[1:]))
        else:
            yolo_coords.extend(map(float, data))

    # Save the last annotation
    if current_label is not None and yolo_coords:
        points = convert_yolo_to_ls(yolo_coords, original_width, original_height)
        polygon_label = class_names[current_label]
        unique_id = generate_unique_id(existing_ids)

        result = {
            "original_width": original_width,
            "original_height": original_height,
            "image_rotation": 0,
            "value": {
                "points": points,
                "closed": True,
                "polygonlabels": [polygon_label]
            },
            "id": unique_id,
            "from_name": "label",
            "to_name": "image",
            "type": "polygonlabels",
            "origin": "manual"
        }

        results.append(result)

    return results





def process_data(input_dir, image_dimensions, image_root_url):
    datas = []
    existing_ids = set()
    
    labels_dir = os.path.join(input_dir, 'labels')
    images_dir = os.path.join(input_dir, 'images')
    
    # Read class names
    class_names = []
    with open(os.path.join(input_dir, 'classes.txt'), 'r') as file:
        class_names = [line.strip() for line in file.readlines()]

    for filename in os.listdir(labels_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(labels_dir, filename)
            annotation_id = os.path.splitext(filename)[0]
            current_time = datetime.now().isoformat()

            # Construct the image file path
            image_file_path = f"{image_root_url}/{annotation_id}.jpg".replace("\\", "/")

            results = process_yolo_file(file_path, image_dimensions, existing_ids, class_names)

            data = {"image": image_file_path}

        datas.append(data)
    return datas




def process_folder(input_dir, image_dimensions, image_root_url):
    tasks = []
    existing_ids = set()
    
    labels_dir = os.path.join(input_dir, 'labels')
    images_dir = os.path.join(input_dir, 'images')
    
    # Read class names
    class_names = []
    with open(os.path.join(input_dir, 'classes.txt'), 'r') as file:
        class_names = [line.strip() for line in file.readlines()]

    for filename in os.listdir(labels_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(labels_dir, filename)
            annotation_id = os.path.splitext(filename)[0]
            current_time = datetime.now().isoformat()

            # Construct the image file path
            image_file_path = f"{image_root_url}/{annotation_id}.jpg".replace("\\", "/")

            results = process_yolo_file(file_path, image_dimensions, existing_ids, class_names)


            task = {
                "data": {
                    "image": image_file_path,
                    "id": annotation_id,
                    "created_username": "saifeldin.darwish.ext@valeo.com",
                    "created_ago": "just now",
                    "completed_by": {
                        "id": 1,
                        "first_name": "",
                        "last_name": "",
                        "avatar": None,
                        "email": "saifeldin.darwish.ext@valeo.com",
                        "initials": "sa"
                    }
                },
                "annotations":[{
                    "result": results,
                    "was_cancelled": False,
                    "ground_truth": False,
                    "created_at": current_time,
                    "updated_at": current_time,
                    "draft_created_at": current_time,
                    "lead_time": 0,
                    "import_id": None,
                    "last_action": None,
                    "task": 0,
                    "project": 0,
                    "updated_by": 1,
                    "parent_prediction": None,
                    "parent_annotation": None,
                    "last_created_by": None
                }]
                
            }

            tasks.append(task)
    return tasks


# Example usage:
# Define the folder containing YOLOv8 text files and the classes.txt file
input_dir = r'C:\Users\sdarwish\snow_potholes_pre'

# Define the image dimensions (these should match the dimensions of the images corresponding to the YOLOv8 annotations)
#image size is not important as YOLOv8 output already outputs the coordinatres as a ratio between (1~0)
image_dimensions = {
    "original_width": 640,
    "original_height": 640
}

# Define the root path for images
image_root_url = "/data/local-files/?d=images"

# Process all YOLOv8 files in the folder and generate the Label Studio JSON format
tasks = process_folder(input_dir, image_dimensions, image_root_url)


# Print the JSON output
output_json = json.dumps(tasks, indent=4)
print(output_json)

# Save the JSON output to the file
output_file_path = 'annotations.json'
with open(output_file_path, 'w') as output_file:
    json.dump(tasks, output_file, indent=4)
