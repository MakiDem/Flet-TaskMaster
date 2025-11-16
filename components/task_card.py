import flet as ft


def create_taskcard(task_text="Task", is_completed=True):
    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text(
                    task_text,
                    size=14,
                    color="#1f2937",
                    no_wrap=False,  # Allow wrapping
                    max_lines=3  # Optional: limit to 3 lines
                ),
                expand=True,  # Takes all available space
                padding=ft.padding.only(right=10)  # Space before checkbox
            ),
            ft.Checkbox(
                value=is_completed, 
                fill_color="#6366f1",
                # Keep checkbox at top when text wraps
            ),
        ], 
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
        bgcolor="#e0e7ff",
        padding=12,
        border_radius=8
    )