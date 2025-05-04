import flet as ft

class SidebarMenu(ft.Container):
    def __init__(self):
        super().__init__(
            width=250,
            bgcolor=ft.colors.BLUE_50,
            content=ft.Column(
                controls=[
                    ft.Text("📡 TechSolutions", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                    ft.Divider(),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.CAMERA_ALT),
                        title=ft.Text("Xem Camera"),
                        on_click=lambda _: print("Chuyển tới Camera")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SETTINGS),
                        title=ft.Text("Cấu Hình"),
                        on_click=lambda _: print("Chuyển tới cấu hình")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.INSERT_CHART),
                        title=ft.Text("Báo Cáo"),
                        on_click=lambda _: print("Chuyển tới báo cáo")
                    ),
                ]
            )
        )
