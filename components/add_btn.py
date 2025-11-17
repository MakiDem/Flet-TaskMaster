import flet as ft

def create_addbtn(page, on_click_handler):
    """
    Create add task button
    
    Args:
        page: Flet page object
        on_click_handler: Function to call when button is clicked
    """
    return ft.Container(
        content=ft.Row([
            ft.Icon("add", color="#ffffff", size=20),
            ft.Text("Create Task", size=14, color="#ffffff", weight=ft.FontWeight.W_500)
        ], alignment="center", spacing=10),
        bgcolor="#6366f1",
        padding=15,
        border_radius=8,
        on_click=on_click_handler,
        ink=True
    )