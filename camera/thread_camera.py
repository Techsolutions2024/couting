import concurrent.futures
import cv2
import base64
import time
import threading
from config.config import load_config
import flet as ft

class CameraThread:
    def __init__(self, camera_id, video_path, counting_classes, confidence_threshold, update_callback):
        self.camera_id = camera_id
        self.video_path = video_path
        self.counting_classes = counting_classes
        self.confidence_threshold = confidence_threshold
        self.update_callback = update_callback
        self.running = False
        self.status = "disconnected"
        self.cap = None
        self.in_count = 0
        self.out_count = 0
        self.total_count = 0
        self.lock = threading.Lock()

    def start(self):
        self.running = True
        self.status = "connecting"
        try:
            self.cap = cv2.VideoCapture(self.video_path)
            if self.cap.isOpened():
                self.status = "connected"
            else:
                self.status = "disconnected"
                self.running = False
                return
        except Exception as e:
            print(f"Camera {self.camera_id} failed to connect: {e}")
            self.status = "disconnected"
            self.running = False
            return

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                self.status = "disconnected"
                break

            # Simulate YOLO processing (placeholder)
            processed_frame, counts = self.process_frame(frame)
            with self.lock:
                self.in_count += counts.get("in", 0)
                self.out_count += counts.get("out", 0)
                self.total_count = self.in_count + self.out_count

            # Convert frame to base64 for UI display
            _, buffer = cv2.imencode(".jpg", processed_frame)
            frame_base64 = base64.b64encode(buffer).decode("utf-8")
            frame_src = f"data:image/jpeg;base64,{frame_base64}"

            # Update UI via callback
            self.update_callback(
                camera_name=f"Camera {self.camera_id}",
                status=self.status,
                in_count=self.in_count,
                out_count=self.out_count,
                total_count=self.total_count,
                frame_src=frame_src,
                object_type=", ".join(self.counting_classes),
            )

            time.sleep(1 / 30)  # Simulate 30 FPS

        if self.cap:
            self.cap.release()
        self.status = "disconnected"

    def process_frame(self, frame):
        # Placeholder for YOLO processing
        # Simulate object detection and counting
        counts = {"in": 0, "out": 0}  # Replace with actual YOLO counts
        return frame, counts

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.status = "disconnected"

class CameraManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = load_config()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        self.cameras = {}
        self.update_callbacks = {}

    def start_cameras(self):
        self.config = load_config()
        num_cameras = self.config.get("num_cameras", 1)
        counting_classes = self.config.get("counting_classes", [])
        confidence_threshold = self.config.get("confidence_threshold", 0.5)

        for i in range(1, num_cameras + 1):
            video_path = self.config.get(f"camera_{i}_video_path", "")
            if video_path and i not in self.cameras:
                camera = CameraThread(
                    camera_id=i,
                    video_path=video_path,
                    counting_classes=counting_classes,
                    confidence_threshold=confidence_threshold,
                    update_callback=self.create_update_callback(i),
                )
                self.cameras[i] = camera
                self.executor.submit(camera.start)

    def create_update_callback(self, camera_id):
        def callback(camera_name, status, in_count, out_count, total_count, frame_src, object_type):
            # Ensure UI updates are thread-safe
            def update_ui():
                try:
                    # Update CameraWidget via page client storage or direct control access
                    self.page.client_storage.set(
                        f"camera_{camera_id}_data",
                        {
                            "name": camera_name,
                            "status": status,
                            "in_count": in_count,
                            "out_count": out_count,
                            "total_count": total_count,
                            "frame_src": frame_src,
                            "object_type": object_type,
                        },
                    )
                    self.page.update()
                except Exception as e:
                    print(f"Error updating UI for Camera {camera_id}: {e}")
            self.page.run_thread_safe(update_ui)
        return callback

    def stop_cameras(self):
        for camera in self.cameras.values():
            camera.stop()
        self.cameras.clear()
        self.executor.shutdown(wait=True)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)

    def get_camera_data(self, camera_id):
        return self.page.client_storage.get(f"camera_{camera_id}_data") or {
            "name": f"Camera {camera_id}",
            "status": "disconnected",
            "in_count": 0,
            "out_count": 0,
            "total_count": 0,
            "frame_src": "https://via.placeholder.com/150",
            "object_type": "Unknown",
        }