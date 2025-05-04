# ui/config_ui.py

import flet as ft
from config import load_config, save_config

def ConfigView():
    config = load_config()

    model_path = ft.TextField(label="Đường dẫn YOLO model", value=config["yolo_model_path"])
    counting_classes = ft.TextField(label="Các class cần đếm (phân cách bằng dấu phẩy)", value=",".join(config["counting_classes"]))
    confidence_slider = ft.Slider(min=0.1, max=1.0, divisions=9, value=config["confidence_threshold"], label="{value:.1f}")
    roi_mode = ft.Dropdown(
        label="Chế độ ROI",
        value=config["roi_mode"],
        options=[
            ft.dropdown.Option("line"),
            ft.dropdown.Option("zone")
        ]
    )
    display_annotated = ft.Switch(label="Hiển thị bounding boxes", value=config["display_annotated"])
    save_csv = ft.Switch(label="Lưu kết quả vào CSV", value=config["save_csv"])
    display_fps = ft.Switch(label="Hiển thị FPS", value=config["display_fps"])
    save_message = ft.Text("", color=ft.colors.GREEN)

    def on_save(e):
        new_config = {
            "yolo_model_path": model_path.value,
            "counting_classes": [cls.strip() for cls in counting_classes.value.split(",") if cls.strip()],
            "confidence_threshold": confidence_slider.value,
            "roi_mode": roi_mode.value,
            "display_annotated": display_annotated.value,
            "save_csv": save_csv.value,
            "display_fps": display_fps.value
        }
        save_config(new_config)
        save_message.value = "✅ Đã lưu cấu hình thành công!"
        save_message.update()

    return ft.Column([
        ft.Text("⚙️ Cấu hình hệ thống", style="headlineSmall"),
        model_path,
        counting_classes,
        confidence_slider,
        roi_mode,
        display_annotated,
        save_csv,
        display_fps,
        ft.ElevatedButton("💾 Lưu cấu hình", on_click=on_save),
        save_message
    ], scroll=ft.ScrollMode.AUTO, expand=True)
