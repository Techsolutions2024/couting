# ui/config_ui.py

import flet as ft
from config.config import load_config, save_config


def ConfigView():
    config = load_config()

    # Cấu hình mô hình AI
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
        min=0.1,
        max=1.0,
        divisions=9,
        value=config["confidence_threshold"],
        label=f"{config['confidence_threshold']:.1f}",
    )

    # Cấu hình camera
    camera_controls = []
    num_cameras = config.get("num_cameras", 1)

    def add_camera_controls():
        for i in range(1, num_cameras + 1):
            camera_controls.append(
                ft.Column([
                    ft.Text(f"Camera {i}:", style="headlineSmall"),
                    ft.Row([
                        ft.Text("Địa chỉ IP hoặc RTSP:"),
                        ft.TextField(value=config.get(f"camera_{i}_video_path", ""), width=400)
                    ]),
                    ft.Row([
                        ft.Text("Chế độ ROI:"),
                        ft.Dropdown(
                            value=config.get(f"camera_{i}_roi_mode", "line"),
                            options=[
                                ft.dropdown.Option("line"),
                                ft.dropdown.Option("zone")
                            ],
                            width=150
                        )
                    ]),
                    ft.Row([
                        ft.Text("Hiển thị Bounding Box:"),
                        ft.Switch(value=config.get(f"camera_{i}_display_annotated", True))
                    ]),
                    ft.Row([
                        ft.Text("Lưu CSV kết quả:"),
                        ft.Switch(value=config.get(f"camera_{i}_save_csv", True))
                    ]),
                    ft.Row([
                        ft.Text("FPS trên video:"),
                        ft.Switch(value=config.get(f"camera_{i}_display_fps", True))
                    ]),
                    ft.Row([
                        ft.ElevatedButton("Xóa camera", icon=ft.icons.DELETE, on_click=lambda e, camera_id=i: on_delete_camera(camera_id))
                    ])
                ])
            )

    def on_add_camera(e):
        nonlocal num_cameras
        num_cameras += 1
        add_camera_controls()
        page.update()

    def on_delete_camera(camera_id):
        nonlocal num_cameras
        num_cameras -= 1
        # Xoá thông tin camera trong cấu hình
        config.pop(f"camera_{camera_id}_video_path", None)
        config.pop(f"camera_{camera_id}_roi_mode", None)
        config.pop(f"camera_{camera_id}_display_annotated", None)
        config.pop(f"camera_{camera_id}_save_csv", None)
        config.pop(f"camera_{camera_id}_display_fps", None)
        add_camera_controls()
        page.update()

    add_camera_controls()

    # Cấu hình đầu vào và đầu ra
    display_annotated_switch = ft.Switch(
        label="🖼️ Hiển thị Bounding Boxes (Toàn bộ hệ thống)",
        value=config.get("display_annotated", True)
    )

    save_csv_switch = ft.Switch(
        label="💾 Lưu kết quả vào CSV (Toàn bộ hệ thống)",
        value=config.get("save_csv", True)
    )

    display_fps_switch = ft.Switch(
        label="📊 Hiển thị FPS trên video (Toàn bộ hệ thống)",
        value=config.get("display_fps", True)
    )

    status_text = ft.Text("", color=ft.colors.GREEN)

    def on_save_config(e):
        new_config = {
            "yolo_model_path": model_path_field.value,
            "counting_classes": [cls.strip() for cls in counting_classes_field.value.split(",") if cls.strip()],
            "confidence_threshold": confidence_slider.value,
            "display_annotated": display_annotated_switch.value,
            "save_csv": save_csv_switch.value,
            "display_fps": display_fps_switch.value,
            "num_cameras": num_cameras,  # Cập nhật số lượng camera
        }

        # Lưu cấu hình cho từng camera
        for i in range(1, num_cameras + 1):
            new_config[f"camera_{i}_video_path"] = camera_controls[i-1].controls[0].value
            new_config[f"camera_{i}_roi_mode"] = camera_controls[i-1].controls[1].controls[1].value
            new_config[f"camera_{i}_display_annotated"] = camera_controls[i-1].controls[2].controls[1].value
            new_config[f"camera_{i}_save_csv"] = camera_controls[i-1].controls[3].controls[1].value
            new_config[f"camera_{i}_display_fps"] = camera_controls[i-1].controls[4].controls[1].value

        save_config(new_config)
        status_text.value = "✅ Cấu hình đã được lưu thành công!"
        status_text.color = ft.colors.GREEN
        status_text.update()

    return ft.Column(
        controls=[
            ft.Text("⚙️ Cấu hình hệ thống", style="headlineSmall"),
            # Mô hình AI
            ft.Text("🔧 Cấu hình Mô hình AI", style="headlineSmall"),
            model_path_field,
            counting_classes_field,
            confidence_slider,
            # Camera
            ft.Text("📸 Cấu hình Camera", style="headlineSmall"),
            *camera_controls,  # Hiển thị cấu hình cho từng camera
            ft.ElevatedButton("Thêm camera", icon=ft.icons.ADD, on_click=on_add_camera),
            # Đầu vào / Đầu ra
            ft.Text("📤 Cấu hình Đầu ra", style="headlineSmall"),
            display_annotated_switch,
            save_csv_switch,
            display_fps_switch,
            # Lưu cấu hình
            ft.ElevatedButton("💾 Lưu cấu hình", icon=ft.icons.SAVE, on_click=on_save_config),
            status_text
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=10
    )
