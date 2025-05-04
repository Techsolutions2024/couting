from ui.widgets import SidebarMenu
import flet as ft

class MainLayout:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        sidebar = SidebarMenu()
        self.content_area = ft.Container(
            content=ft.Text("Chọn chức năng từ menu bên trái"),
            expand=True,
            padding=20
        )

        return ft.Row(
            controls=[
                sidebar,
                self.content_area
            ],
            expand=True
        )
