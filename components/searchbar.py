import flet as ft

def create_searchbar():
    return ft.Container(
        content=ft.Row([
            ft.Icon("search", color="#9ca3af", size=20),
            ft.TextField(
                hint_text="Search for Task..",
                border=ft.InputBorder.NONE,
                text_size=14,
                expand=True
            ),
            ft.IconButton(
                icon="add",
                icon_color="#6366f1",
                bgcolor="#e0e7ff",
                icon_size=20
            )
        ], spacing=10),
        bgcolor="#ffffff",
        padding=ft.padding.only(left=15, right=5, top=5, bottom=5),
        border_radius=10
    )