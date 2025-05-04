import json
import os

class ROIManager:
    def __init__(self, roi_dir="roi_data"):
        self.roi_dir = roi_dir
        os.makedirs(self.roi_dir, exist_ok=True)

    def get_roi_path(self, camera_id):
        return os.path.join(self.roi_dir, f"{camera_id}.json")

    def save_roi(self, camera_id, roi_data):
        path = self.get_roi_path(camera_id)
        with open(path, "w") as f:
            json.dump(roi_data, f, indent=2)

    def load_roi(self, camera_id):
        path = self.get_roi_path(camera_id)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return json.load(f)
