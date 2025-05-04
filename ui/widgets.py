import flet as ft

def SidebarMenu(on_select):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("📋 MENU", weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(),
                ft.ListTile(
                    title=ft.Text("📷 Xem Camera"),
                    on_click=lambda _: on_select("camera"),
                ),
                ft.ListTile(
                    title=ft.Text("⚙️ Cấu hình hệ thống"),
                    on_click=lambda _: on_select("config"),
                ),
                ft.ListTile(
                    title=ft.Text("📊 Xem báo cáo"),
                    on_click=lambda _: on_select("report"),
                ),
                ft.ListTile(
                    title=ft.Text("📌 Vùng ROI"),
                    on_click=lambda _: on_select("roi"),
                ),
                ft.ListTile(
                    title=ft.Text("💡 Hướng dẫn"),
                    on_click=lambda _: on_select("help"),
                ),
            ],
            width=250,
        ),
        bgcolor="white",
        border=ft.border.all(1, "gray"),
        padding=10,
    )

def CameraWidget(camera_name, camera_status, in_count, out_count, total_count, object_type, on_click_callback):
    # Status icon for connection
    status_icon = ft.Icon(
        name=ft.icons.CIRCLE,
        color="green" if camera_status == "connected" else "red",
        size=14,
    )

    # Statistics display
    stats = ft.Column(
        [
            ft.Text(f"IN: {in_count}", size=12),
            ft.Text(f"OUT: {out_count}", size=12),
            ft.Text(f"TOTAL: {total_count}", size=12),
            ft.Text(f"Type: {object_type}", size=12),
        ],
        spacing=2,
    )

    # Control bar for each camera
    controls = ft.Row(
        [
            ft.IconButton(
                icon=ft.icons.PLAY_ARROW,
                tooltip="Tạm dừng/Phát",
                on_click=lambda _: print(f"Tạm dừng/Phát camera {camera_name}"),
            ),
            ft.IconButton(
                icon=ft.icons.REFRESH,
                tooltip="Làm mới",
                on_click=lambda _: print(f"Làm mới camera {camera_name}"),
            ),
            ft.IconButton(
                icon=ft.icons.ZOOM_OUT_MAP,
                tooltip="Phóng to",
                on_click=lambda _: print(f"Phóng to camera {camera_name}"),
            ),
            ft.IconButton(
                icon=ft.icons.EDIT,
                tooltip="Chỉnh sửa ROI",
                on_click=lambda _: print(f"Chỉnh sửa ROI cho camera {camera_name}"),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Camera widget
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        status_icon,
                        ft.Text(camera_name, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.Image(
                        src="https://via.placeholder.com/150",  # Placeholder for YOLO frame
                        height=150,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    on_click=lambda _: on_click_callback(camera_name),
                ),
                stats,
                controls,
            ],
            spacing=5,
        ),
        
        padding=10,
        border_radius=8,  # Fixed: Replaced ft.BorderRadius.all(8) with 8
        border=ft.border.all(1, "black"),
        bgcolor="white",
        expand=True,
    )