import os
import flet as ft
from config.config import load_config, save_config

def ConfigView(page: ft.Page):
    config = load_config()

    # Status text for feedback
    status_text = ft.Text("", color=ft.colors.GREEN_700, size=14)

    # File picker for model selection
    model_picker = ft.FilePicker(on_result=lambda e: on_model_pick(e))
    model_path_field = ft.TextField(
        label="📁 Đường dẫn YOLO Model",
        value=config.get("yolo_model_path", ""),
        width=400,
        read_only=True,
        tooltip="Chọn file mô hình YOLO (.pt)",
    )
    model_pick_button = ft.ElevatedButton(
        "Chọn Model",
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: model_picker.get_directory_path(),
        tooltip="Mở trình duyệt để chọn file mô hình YOLO",
    )

    def on_model_pick(e):
        if e.path:
            model_path_field.value = os.path.join(e.path, e.file_name) if e.file_name else e.path
            model_path_field.update()

    # File picker for video input
    video_picker = ft.FilePicker(on_result=lambda e: on_video_pick(e))
    video_path_field = ft.TextField(
        label="🎥 Đường dẫn Video đầu vào",
        value=config.get("video_path", ""),
        width=400,
        read_only=True,
        tooltip="Chọn file video (.mp4)",
    )
    video_pick_button = ft.ElevatedButton(
        "Chọn Video",
        icon=ft.icons.VIDEO_FILE,
        on_click=lambda _: video_picker.pick_files(allowed_extensions=["mp4"]),
        tooltip="Mở trình duyệt để chọn file video",
    )

    def on_video_pick(e):
        if e.files:
            video_path_field.value = e.files[0].path
            video_path_field.update()

    # File picker for output directory
    output_picker = ft.FilePicker(on_result=lambda e: on_output_pick(e))
    output_path_field = ft.TextField(
        label="📂 Thư mục lưu kết quả",
        value=config.get("output_dir", ""),
        width=400,
        read_only=True,
        tooltip="Chọn thư mục để lưu kết quả (CSV, video, ...)",
    )
    output_pick_button = ft.ElevatedButton(
        "Chọn Thư mục",
        icon=ft.icons.FOLDER,
        on_click=lambda _: output_picker.get_directory_path(),
        tooltip="Mở trình duyệt để chọn thư mục lưu kết quả",
    )

    def on_output_pick(e):
        if e.path:
            output_path_field.value = e.path
            output_path_field.update()

    # Counting classes
    counting_classes_field = ft.TextField(
        label="🔢 Các class cần đếm (cách nhau bằng dấu phẩy)",
        value=",".join(config.get("counting_classes", [])),
        width=400,
        tooltip="Nhập các lớp đối tượng, ví dụ: person, car, truck",
    )

    # Confidence threshold
    confidence_slider = ft.Slider(
        min=0.1,
        max=1.0,
        divisions=9,
        value=config.get("confidence_threshold", 0.5),
        label="{value:.1f}",
        width=400,
        on_change=lambda e: update_confidence_label(e),
        tooltip="Ngưỡng tin cậy cho việc phát hiện đối tượng",
    )

    def update_confidence_label(e):
        confidence_slider.label = f"{e.control.value:.1f}"
        confidence_slider.update()

    # Camera configuration
    camera_controls = ft.Column(spacing=10)
    num_cameras = config.get("num_cameras", 1)

    def add_camera_controls():
        camera_controls.controls.clear()
        for i in range(1, num_cameras + 1):
            camera_controls.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Camera {i}", weight=ft.FontWeight.BOLD, size=16),
                            ft.TextField(
                                label="Địa chỉ IP hoặc RTSP",
                                value=config.get(f"camera_{i}_video_path", ""),
                                width=350,
                                tooltip="Nhập URL RTSP hoặc IP của camera",
                            ),
                            ft.Dropdown(
                                label="Chế độ ROI",
                                value=config.get(f"camera_{i}_roi_mode", "line"),
                                options=[
                                    ft.dropdown.Option("line", text="Line"),
                                    ft.dropdown.Option("zone", text="Zone"),
                                ],
                                width=200,
                                tooltip="Chọn chế độ vùng quan tâm (ROI)",
                            ),
                            ft.Switch(
                                label="Hiển thị Bounding Box",
                                value=config.get(f"camera_{i}_display_annotated", True),
                                tooltip="Bật/tắt hiển thị khung bao quanh đối tượng",
                            ),
                            ft.Switch(
                                label="Lưu CSV kết quả",
                                value=config.get(f"camera_{i}_save_csv", True),
                                tooltip="Bật/tắt lưu kết quả vào file CSV",
                            ),
                            ft.Switch(
                                label="Hiển thị FPS",
                                value=config.get(f"camera_{i}_display_fps", True),
                                tooltip="Bật/tắt hiển thị FPS trên video",
                            ),
                            ft.ElevatedButton(
                                "Xóa Camera",
                                icon=ft.icons.DELETE,
                                on_click=lambda e, idx=i: on_delete_camera(idx),
                                tooltip="Xóa camera này",
                                color=ft.colors.RED_700,
                            ),
                        ], spacing=10),
                        padding=10,
                    ),
                    elevation=2,
                )
            )
        page.update()

    def on_add_camera(e):
        nonlocal num_cameras
        num_cameras += 1
        config["num_cameras"] = num_cameras
        add_camera_controls()

    def on_delete_camera(camera_id):
        nonlocal num_cameras
        if num_cameras > 1:
            num_cameras -= 1
            config["num_cameras"] = num_cameras
            # Remove camera config
            for i in range(camera_id, num_cameras + 1):
                config[f"camera_{i}_video_path"] = config.get(f"camera_{i+1}_video_path", "")
                config[f"camera_{i}_roi_mode"] = config.get(f"camera_{i+1}_roi_mode", "line")
                config[f"camera_{i}_display_annotated"] = config.get(f"camera_{i+1}_display_annotated", True)
                config[f"camera_{i}_save_csv"] = config.get(f"camera_{i+1}_save_csv", True)
                config[f"camera_{i}_display_fps"] = config.get(f"camera_{i+1}_display_fps", True)
            # Clear the last camera's config
            config.pop(f"camera_{num_cameras+1}_video_path", None)
            config.pop(f"camera_{num_cameras+1}_roi_mode", None)
            config.pop(f"camera_{num_cameras+1}_display_annotated", None)
            config.pop(f"camera_{num_cameras+1}_save_csv", None)
            config.pop(f"camera_{num_cameras+1}_display_fps", None)
            add_camera_controls()

    add_camera_controls()

    # Global output settings
    display_annotated_switch = ft.Switch(
        label="🖼️ Hiển thị Bounding Boxes (Toàn bộ)",
        value=config.get("display_annotated", True),
        tooltip="Bật/tắt hiển thị khung bao quanh đối tượng cho toàn bộ hệ thống",
    )
    save_csv_switch = ft.Switch(
        label="💾 Lưu kết quả vào CSV (Toàn bộ)",
        value=config.get("save_csv", True),
        tooltip="Bật/tắt lưu kết quả vào file CSV cho toàn bộ hệ thống",
    )
    display_fps_switch = ft.Switch(
        label="📊 Hiển thị FPS (Toàn bộ)",
        value=config.get("display_fps", True),
        tooltip="Bật/tắt hiển thị FPS trên video cho toàn bộ hệ thống",
    )

    def on_save_config(e):
        if not model_path_field.value:
            status_text.value = "❌ Vui lòng chọn file mô hình YOLO!"
            status_text.color = ft.colors.RED_700
            status_text.update()
            return
        if not counting_classes_field.value.strip():
            status_text.value = "❌ Vui lòng nhập ít nhất một class cần đếm!"
            status_text.color = ft.colors.RED_700
            status_text.update()
            return

        new_config = {
            "yolo_model_path": model_path_field.value,
            "video_path": video_path_field.value,
            "output_dir": output_path_field.value,
            "counting_classes": [cls.strip() for cls in counting_classes_field.value.split(",") if cls.strip()],
            "confidence_threshold": confidence_slider.value,
            "display_annotated": display_annotated_switch.value,
            "save_csv": save_csv_switch.value,
            "display_fps": display_fps_switch.value,
            "num_cameras": num_cameras,
        }

        # Save camera configurations
        for i in range(num_cameras):
            new_config[f"camera_{i+1}_video_path"] = camera_controls.controls[i].content.content.controls[1].value
            new_config[f"camera_{i+1}_roi_mode"] = camera_controls.controls[i].content.content.controls[2].value
            new_config[f"camera_{i+1}_display_annotated"] = camera_controls.controls[i].content.content.controls[3].value
            new_config[f"camera_{i+1}_save_csv"] = camera_controls.controls[i].content.content.controls[4].value
            new_config[f"camera_{i+1}_display_fps"] = camera_controls.controls[i].content.content.controls[5].value

        save_config(new_config)
        status_text.value = "✅ Cấu hình đã được lưu thành công!"
        status_text.color = ft.colors.GREEN_700
        status_text.update()

    def on_reset_config(e):
        nonlocal config
        config = {
            "yolo_model_path": "",
            "video_path": "",
            "output_dir": "",
            "counting_classes": [],
            "confidence_threshold": 0.5,
            "display_annotated": True,
            "save_csv": True,
            "display_fps": True,
            "num_cameras": 1,
            "camera_1_video_path": "",
            "camera_1_roi_mode": "line",
            "camera_1_display_annotated": True,
            "camera_1_save_csv": True,
            "camera_1_display_fps": True,
        }
        model_path_field.value = ""
        video_path_field.value = ""
        output_path_field.value = ""
        counting_classes_field.value = ""
        confidence_slider.value = 0.5
        display_annotated_switch.value = True
        save_csv_switch.value = True
        display_fps_switch.value = True
        nonlocal num_cameras
        num_cameras = 1
        add_camera_controls()
        status_text.value = "🔄 Đã đặt lại cấu hình mặc định!"
        status_text.color = ft.colors.BLUE_700
        status_text.update()

    # Add file pickers to page
    page.overlay.extend([model_picker, video_picker, output_picker])

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("⚙️ Cấu hình Hệ thống", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🔧 Cấu hình Mô hình AI", size=16, weight=ft.FontWeight.BOLD),
                            ft.Row([model_path_field, model_pick_button], alignment=ft.MainAxisAlignment.START),
                            ft.Row([video_path_field, video_pick_button], alignment=ft.MainAxisAlignment.START),
                            ft.Row([output_path_field, output_pick_button], alignment=ft.MainAxisAlignment.START),
                            counting_classes_field,
                            ft.Row([
                                ft.Text("Ngưỡng Confidence:", tooltip="Ngưỡng tin cậy cho việc phát hiện đối tượng"),
                                confidence_slider,
                            ]),
                        ], spacing=10),
                        padding=10,
                    ),
                    elevation=2,
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("📸 Cấu hình Camera", size=16, weight=ft.FontWeight.BOLD),
                                ft.ElevatedButton(
                                    "Thêm Camera",
                                    icon=ft.icons.ADD,
                                    on_click=on_add_camera,
                                    tooltip="Thêm một camera mới",
                                    color=ft.colors.GREEN_700,
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            camera_controls,
                        ], spacing=10),
                        padding=10,
                    ),
                    elevation=2,
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("📤 Cấu hình Đầu ra", size=16, weight=ft.FontWeight.BOLD),
                            display_annotated_switch,
                            save_csv_switch,
                            display_fps_switch,
                        ], spacing=10),
                        padding=10,
                    ),
                    elevation=2,
                ),
                ft.Row([
                    ft.ElevatedButton(
                        "💾 Lưu Cấu hình",
                        icon=ft.icons.SAVE,
                        on_click=on_save_config,
                        tooltip="Lưu tất cả các thiết lập",
                        color=ft.colors.BLUE_700,
                    ),
                    ft.ElevatedButton(
                        "🔄 Đặt Lại",
                        icon=ft.icons.RESTORE,
                        on_click=on_reset_config,
                        tooltip="Đặt lại tất cả các thiết lập về mặc định",
                        color=ft.colors.ORANGE_700,
                    ),
                ], alignment=ft.MainAxisAlignment.END),
                status_text,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        expand=True,
    )