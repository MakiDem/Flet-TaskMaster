import flet as ft
from dialogs.add_task_dialog import show_add_task_dialog

def create_addbtn(page):
    """
    Create add task button
    
    Args:
        page: Flet page object
    """
    def on_add_task_click(e):
        show_add_task_dialog(page)  # Now page is the correct object
    
    return ft.Container(
        content=ft.Row([
            ft.Icon("add", color="#ffffff", size=20),
            ft.Text("Create Task", size=14, color="#ffffff", weight=ft.FontWeight.W_500)
        ], alignment="center", spacing=10),
        bgcolor="#6366f1",
        padding=15,
        border_radius=8,
        on_click=lambda e: on_add_task_click(e),
        ink=True
    )