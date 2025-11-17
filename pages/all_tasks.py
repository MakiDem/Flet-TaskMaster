import flet as ft
from components.tasks_frame.color import get_priority_color, get_status_color
from components.tasks_frame.task import create_task_item, create_filter_handler

def create_all_tasks_page_content(page, all_tasks_data, show_add_dialog_handler):
    """
    All Tasks page content
    
    Args:
        page: Flet page object
        all_tasks_data: List of all tasks
        show_add_dialog_handler: Function to show add dialog (from main.py)
    """
    
    # Current filter state
    current_filter = ["all"]
    
    # References
    task_list_ref = ft.Ref[ft.Column]()
    filter_buttons = {}
    
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
    all_btn.on_click = create_filter_handler(page, all_tasks_data, task_list_ref, current_filter, filter_buttons, "all")
    completed_btn.on_click = create_filter_handler(page, all_tasks_data, task_list_ref, current_filter, filter_buttons, "completed")
    pending_btn.on_click = create_filter_handler(page, all_tasks_data, task_list_ref, current_filter, filter_buttons, "pending")
    overdue_btn.on_click = create_filter_handler(page, all_tasks_data, task_list_ref, current_filter, filter_buttons, "overdue")
    
    # Initial task list
    initial_tasks = ft.Column(ref=task_list_ref, spacing=10, scroll="auto")
    
    # Populate initial tasks
    initial_tasks.controls.append(
        ft.Text(f"{len(all_tasks_data)} Tasks", size=14, color="#6b7280", weight=ft.FontWeight.W_500)
    )
    initial_tasks.controls.append(ft.Container(height=10))
    for task in all_tasks_data:
        initial_tasks.controls.append(create_task_item(task))
    
    # Return page content
    return ft.Column([
        # Header
        ft.Row([
            ft.Text("All Tasks", size=28, weight=ft.FontWeight.BOLD, color="#1f2937"),
            ft.Container(expand=True),
            ft.ElevatedButton(
                "Add New Task",
                icon="add",
                bgcolor="#6366f1",
                color="#ffffff",
                on_click=show_add_dialog_handler  # Use the handler from main.py
            )
        ]),
        
        ft.Container(height=20),
        
        # Search and filter
        ft.Row([
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
        ], spacing=10),
        
        ft.Container(height=20),
        
        # Filter tabs
        ft.Row([
            all_btn,
            completed_btn,
            pending_btn,
            overdue_btn,
        ], spacing=8),
        
        ft.Container(height=20),
        
        # Task list
        initial_tasks
    ], scroll="auto")