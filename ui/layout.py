# ui/layout.py
import flet as ft
from .widgets import SidebarMenu

def build(page: ft.Page, content_area: ft.Column):
    def handle_menu_selection(section):
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

    sidebar = SidebarMenu(handle_menu_selection)

    return ft.Row(
        controls=[
            sidebar,
            ft.VerticalDivider(width=1),
            content_area
        ],
        expand=True
    )
