import flet as ft
from components.tasks_frame.task import create_filter_handler


def create_filter_section(page, all_tasks_data, task_list_ref, current_filter, handle_edit_task, handle_delete_task):
    """
    Create filter buttons section.
    
    Returns:
        tuple: (filter_row, filter_buttons_dict)
    """
    
    # Create filter buttons
    all_btn = ft.Container(
        content=ft.Text("All", size=13, color="#6366f1", weight=ft.FontWeight.W_500),
        bgcolor="#e0e7ff",
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=6,
        ink=True
    )
    
    completed_btn = ft.Container(
        content=ft.Text("Completed", size=13, color="#6b7280"),
        bgcolor="#f3f4f6",
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=6,
        ink=True
    )
    
    pending_btn = ft.Container(
        content=ft.Text("Pending", size=13, color="#6b7280"),
        bgcolor="#f3f4f6",
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=6,
        ink=True
    )
    
    overdue_btn = ft.Container(
        content=ft.Text("Overdue", size=13, color="#6b7280"),
        bgcolor="#f3f4f6",
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=6,
        ink=True
    )
    
    # Store buttons in dictionary
    filter_buttons = {
        "all": all_btn,
        "completed": completed_btn,
        "pending": pending_btn,
        "overdue": overdue_btn
    }
    
    # Assign click handlers
    all_btn.on_click = create_filter_handler(page, all_tasks_data, task_list_ref, current_filter, filter_buttons, "all", handle_edit_task, handle_delete_task)
    completed_btn.on_click = create_filter_handler(page, all_tasks_data, task_list_ref, current_filter, filter_buttons, "completed", handle_edit_task, handle_delete_task)
    pending_btn.on_click = create_filter_handler(page, all_tasks_data, task_list_ref, current_filter, filter_buttons, "pending", handle_edit_task, handle_delete_task)
    overdue_btn.on_click = create_filter_handler(page, all_tasks_data, task_list_ref, current_filter, filter_buttons, "overdue", handle_edit_task, handle_delete_task)
    
    # Create row
    filter_row = ft.Row([
        all_btn,
        completed_btn,
        pending_btn,
        overdue_btn,
    ], spacing=8)
    
    return filter_row, filter_buttons