import flet as ft
from .widgets import SidebarMenu, CameraWidget
from ui.config import ConfigView



def build(page: ft.Page, content_area: ft.Column):
    def handle_menu_selection(section):
        content_area.controls.clear()
        if section == "camera":
            content_area.controls.append(build_camera_grid(page))
        elif section == "config":
            content_area.controls.append(ConfigView())

        elif section == "report":
            content_area.controls.append(ft.Text("📊 Reports"))
        elif section == "roi":
            content_area.controls.append(ft.Text("📌 ROI Editor"))
        elif section == "help":
            content_area.controls.append(ft.Text("💡 User Guide"))
        else:
            content_area.controls.append(ft.Text("🚀 Welcome"))
        page.update()

    sidebar = SidebarMenu(handle_menu_selection)

    return ft.Row(
        controls=[
            sidebar,
            ft.VerticalDivider(width=1),
            content_area,
        ],
        expand=True,
    )

def build_camera_grid(page: ft.Page):
    # Sample camera data
    cameras = [
        {"name": f"Camera {i}", "status": "connected" if i % 2 == 0 else "disconnected", 
         "in_count": i * 2, "out_count": i, "total_count": i * 3, "object_type": "Person" if i % 2 == 0 else "Vehicle"}
        for i in range(1, 9)
    ]

    def on_camera_click(camera_name):
        detail_view.controls.clear()
        selected_camera = next((cam for cam in cameras if cam["name"] == camera_name), None)
        if selected_camera:
            detail_view.controls.extend([
                ft.Text(f"Chi tiết cho {camera_name}", size=16, weight="bold"),
                ft.Image(src="https://via.placeholder.com/300", height=200),  # Placeholder for YOLO annotated frame
                ft.Text(f"Metadata: Tên camera: {camera_name}, Type: {selected_camera['object_type']}"),
                ft.Text(f"Trạng thái: {'Kết nối' if selected_camera['status'] == 'connected' else 'Mất kết nối'}"),
                ft.Text("Logs: Không có logs gần đây"),
            ])
        page.update()

    # Toolbar components
    grid_layout = ft.Dropdown(
        label="Grid Layout",
        options=[
            ft.dropdown.Option("2x2"),
            ft.dropdown.Option("3x3"),
            ft.dropdown.Option("4x4"),
        ],
        value="2x2",
        on_change=lambda e: update_grid_layout(grid_layout.value),
        width=150,
    )

    object_filter = ft.Dropdown(
        label="Lọc đối tượng",
        options=[
            ft.dropdown.Option("All"),
            ft.dropdown.Option("Person"),
            ft.dropdown.Option("Vehicle"),
        ],
        value="All",
        on_change=lambda e: update_camera_grid(object_filter.value, search_field.value),
        width=150,
    )

    search_field = ft.TextField(
        hint_text="Tìm kiếm camera...",
        on_change=lambda e: update_camera_grid(object_filter.value, search_field.value),
        width=300,
    )

    # Camera grid
    grid_view = ft.GridView(
        expand=True,
        runs_count=2,  # Default 2x2
        spacing=10,
        run_spacing=10,
    )

    # Right panel for camera details
    detail_view = ft.Column(
        [
            ft.Text("Chọn camera để xem chi tiết", size=14, weight="bold"),
            ft.Image(src="https://via.placeholder.com/300", height=200),
            ft.Text("Metadata: None"),
            ft.Text("Logs: None"),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
    )

    def update_grid_layout(layout):
        if layout == "2x2":
            grid_view.runs_count = 2
        elif layout == "3x3":
            grid_view.runs_count = 3
        elif layout == "4x4":
            grid_view.runs_count = 4
        update_camera_grid(object_filter.value, search_field.value)

    def update_camera_grid(object_type, search_text):
        grid_view.controls.clear()
        filtered_cameras = cameras
        if object_type != "All":
            filtered_cameras = [cam for cam in filtered_cameras if cam["object_type"] == object_type]
        if search_text:
            filtered_cameras = [cam for cam in filtered_cameras if search_text.lower() in cam["name"].lower()]
        
        for cam in filtered_cameras:
            grid_view.controls.append(
                CameraWidget(
                    camera_name=cam["name"],
                    camera_status=cam["status"],
                    in_count=cam["in_count"],
                    out_count=cam["out_count"],
                    total_count=cam["total_count"],
                    object_type=cam["object_type"],
                    on_click_callback=on_camera_click,
                )
            )
        page.update()

    # Initial grid population
    update_camera_grid("All", "")

    # Overall layout
    return ft.Column(
        [
            ft.Container(
                content=ft.Row(
                    [
                        grid_layout,
                        object_filter,
                        search_field,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=10,
            ),
            ft.Row(
                [
                    ft.Container(content=grid_view, expand=3, padding=10),
                    ft.Container(content=detail_view, expand=1, bgcolor="lightgray", padding=10),
                ],
                expand=True,
            ),
        ],
        expand=True,
    )