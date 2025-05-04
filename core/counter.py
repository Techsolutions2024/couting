import csv
from datetime import datetime
from config import CSV_COLUMNS, DEFAULT_OUTPUT_DIR
import os

class ObjectCounter:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.count_data = {}

    def count(self, detections, class_names):
        self.count_data.clear()
        for cls in class_names:
            self.count_data[cls] = 0

        for class_id in detections.class_id:
            class_name = class_names[class_id]
            if class_name in self.count_data:
                self.count_data[class_name] += 1

        return self.count_data

    def save_to_csv(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(DEFAULT_OUTPUT_DIR, f"{self.camera_id}_count.csv")

        with open(filepath, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            if f.tell() == 0:
                writer.writeheader()
            for cls, count in self.count_data.items():
                writer.writerow({
                    "timestamp": now,
                    "camera_id": self.camera_id,
                    "class_name": cls,
                    "count": count
                })
