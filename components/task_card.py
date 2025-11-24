import flet as ft


def create_taskcard(task_text="Task", is_completed=False):
    """
    Create a styled task card for dashboard.
    
    Args:
        task_text: Task description
        is_completed: Whether task is completed
    
    Returns:
        ft.Container: Styled task card
    """
    return ft.Container(
        content=ft.Row([
            # Checkbox on the left
            ft.Checkbox(
                value=is_completed, 
                fill_color="#6366f1",
                check_color="#ffffff",
            ),
            # Task text
            ft.Container(
                content=ft.Text(
                    task_text,
                    size=14,
                    color="#70757e" if is_completed else "#1f2937",
                    weight=ft.FontWeight.W_400,
                    no_wrap=False,
                    max_lines=2,
                    text_align=ft.TextAlign.LEFT,
                ),
                expand=True,
                padding=ft.padding.only(left=5, right=10)
            ),
        ], 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        bgcolor="#ffffff",
        padding=ft.padding.symmetric(horizontal=15, vertical=12),
        border_radius=10,
        border=ft.border.all(1, "#e5e7eb"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=2,
            color="#00000008",
            offset=ft.Offset(0, 1)
        )
    )