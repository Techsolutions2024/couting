import flet as ft
from .widgets import SidebarMenu

def build(page: ft.Page, content_area: ft.Column):
    def handle_menu_selection(section):
        # Xóa nội dung cũ và thêm nội dung mới vào khu vực chính
        content_area.controls.clear()
        if section == "camera":
            content_area.controls.append(ft.Text("🎥 Camera View"))
        elif section == "config":
            content_area.controls.append(ft.Text("⚙️ System Configuration"))
        elif section == "report":
            content_area.controls.append(ft.Text("📊 Reports"))
        elif section == "roi":
            content_area.controls.append(ft.Text("📌 ROI Editor"))
        elif section == "help":
            content_area.controls.append(ft.Text("💡 User Guide"))
        else:
            content_area.controls.append(ft.Text("🚀 Welcome"))
        
        page.update()

    # Sidebar menu
    sidebar = SidebarMenu(handle_menu_selection)

    # Layout chính
    return ft.Row(
        controls=[
            sidebar,  # Sidebar bên trái
            ft.VerticalDivider(width=1),  # Đường phân cách
            content_area  # Khu vực nội dung chính
        ],
        expand=True
    )