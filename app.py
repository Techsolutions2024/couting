import flet as ft
from ui import layout

def main(page: ft.Page):
    page.title = "Object Counter AI"
    page.window_width = 1200
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    content_area = ft.Column(expand=True)
    layout_view = layout.build(page, content_area)

    page.appbar = ft.AppBar(
        title=ft.Text("🧠 Object Counter AI", size=20, weight=ft.FontWeight.BOLD),
        bgcolor=ft.colors.BLUE_600,
        actions=[
            ft.IconButton(
                ft.icons.HELP_OUTLINE,
                tooltip="Trợ giúp",
                on_click=lambda e: content_area.controls.append(ft.Text("💡 Hướng dẫn sử dụng")),
            )
        ]
    )

    page.add(layout_view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)