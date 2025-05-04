from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np
class ObjectDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.box_annotator = sv.BoxAnnotator()

    def detect(self, frame, target_classes=None):
        results = self.model(frame, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)

        # Filter by target classes if provided
        if target_classes:
            detections = detections[np.isin(detections.class_id, [
                self.model.model.names.index(cls) for cls in target_classes if cls in self.model.model.names
            ])]

        annotated = self.box_annotator.annotate(
            scene=frame.copy(),
            detections=detections,
            labels=[self.model.model.names[c] for c in detections.class_id]
        )

        return annotated, detections
