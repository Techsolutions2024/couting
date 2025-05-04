# config/config.py

import json
import os

CONFIG_FILE = "config/system_config.json"

DEFAULT_CONFIG = {
    "yolo_model_path": "data/best.pt",
    "counting_classes": ["person"],
    "confidence_threshold": 0.5,
    "roi_mode": "line",
    "display_annotated": True,
    "save_csv": True,
    "display_fps": True
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
