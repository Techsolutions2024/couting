import flet as ft

def SidebarMenu(on_select):
    return ft.Column(
        width=250,
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
        ]
    )