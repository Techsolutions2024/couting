import flet as ft
from ui.layout import MainLayout
from config import APP_TITLE

def main(page: ft.Page):
    page.title = APP_TITLE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True
    layout = MainLayout(page)
    page.add(layout.build())

if __name__ == "__main__":
    ft.app(target=main)
