import flet as ft


def create_header(show_add_dialog_handler):
    """
    Create the page header.
    
    Args:
        show_add_dialog_handler: Function to show add dialog
    
    Returns:
        ft.Row: Header row
    """
    
    return ft.Row([
        ft.Text("All Tasks", size=28, weight=ft.FontWeight.BOLD, color="#1f2937"),
        ft.Container(expand=True),
        ft.ElevatedButton(
            "Add New Task",
            icon="add",
            bgcolor="#6366f1",
            color="#ffffff",
            on_click=show_add_dialog_handler
        )
    ])