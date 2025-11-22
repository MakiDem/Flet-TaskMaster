import flet as ft


def create_search_bar():
    """
    Create the search and filter row.
    
    Returns:
        ft.Row: Search bar row
    """
    
    return ft.Row([
        ft.Container(
            content=ft.Row([
                ft.Icon("search", color="#9ca3af", size=18),
                ft.TextField(
                    hint_text="Search tasks...",
                    border=ft.InputBorder.NONE,
                    text_size=14,
                    expand=True
                )
            ]),
            bgcolor="#ffffff",
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            border_radius=8,
            border=ft.border.all(1, "#e5e7eb"),
            expand=True
        ),
        
        ft.Container(
            content=ft.Row([
                ft.Icon("filter_list", size=18, color="#6366f1"),
                ft.Text("Filter", size=14, color="#6366f1")
            ], spacing=5),
            bgcolor="#e0e7ff",
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            border_radius=8
        )
    ], spacing=10)