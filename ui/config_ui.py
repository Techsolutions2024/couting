# ui/config_ui.py

import flet as ft
from config.config import load_config, save_config

def ConfigView():
    config = load_config()

    # Các trường nhập cho cấu hình
    model_path_field = ft.TextField(
        label="📁 Đường dẫn YOLO Model",
        value=config.get("yolo_model_path", ""),
        width=500
    )

    counting_classes_field = ft.TextField(
        label="🔢 Các class cần đếm (cách nhau bằng dấu phẩy)",
        value=",".join(config.get("counting_classes", [])),
        width=500
    )

    confidence_slider = ft.Slider(
        label="🎯 Confidence Threshold",
        min=0.1,
        max=1.0,
        divisions=9,
        value=config.get("confidence_threshold", 0.5),
        width=400,
        label="{value:.1f}"
    )

    roi_mode_dropdown = ft.Dropdown(
        label="🗺️ Chế độ ROI",
        value=config.get("roi_mode", "line"),
        options=[
            ft.dropdown.Option("line"),
            ft.dropdown.Option("zone")
        ],
        width=300
    )

    display_annotated_switch = ft.Switch(
        label="🖼️ Hiển thị Bounding Boxes",
        value=config.get("display_annotated", True)
    )

    save_csv_switch = ft.Switch(
        label="💾 Lưu kết quả vào CSV",
        value=config.get("save_csv", True)
    )

    display_fps_switch = ft.Switch(
        label="📊 Hiển thị FPS trên video",
        value=config.get("display_fps", True)
    )

    status_text = ft.Text("", color=ft.colors.GREEN)

    def on_save_config(e):
        new_config = {
            "yolo_model_path": model_path_field.value,
            "counting_classes": [cls.strip() for cls in counting_classes_field.value.split(",") if cls.strip()],
            "confidence_threshold": confidence_slider.value,
            "roi_mode": roi_mode_dropdown.value,
            "display_annotated": display_annotated_switch.value,
            "save_csv": save_csv_switch.value,
            "display_fps": display_fps_switch.value
        }
        save_config(new_config)
        status_text.value = "✅ Cấu hình đã được lưu thành công!"
        status_text.color = ft.colors.GREEN
        status_text.update()

    return ft.Column(
        controls=[
            ft.Text("⚙️ Cấu hình hệ thống", style="headlineSmall"),
            model_path_field,
            counting_classes_field,
            confidence_slider,
            roi_mode_dropdown,
            display_annotated_switch,
            save_csv_switch,
            display_fps_switch,
            ft.ElevatedButton("💾 Lưu cấu hình", icon=ft.icons.SAVE, on_click=on_save_config),
            status_text
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=10
    )
