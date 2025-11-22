import flet as ft
from components.tasks_frame.color import get_priority_color, get_status_color

def create_task_item(task, page, on_edit_task=None, on_delete_task=None):
    """
    Create a single task item
    
    Args:
        task: Task dictionary with id, title, status, priority, date, etc.
        page: Flet page object
        on_edit_task: Callback function when edit is clicked (receives task)
        on_delete_task: Callback function when delete is clicked (receives task_id)
    """
    
    def show_task_menu(e):
        """Show popup menu for task actions"""
        
        def handle_edit(e):
            page.close(menu_dialog)
            if on_edit_task:
                on_edit_task(task)
        
        def handle_delete(e):
            page.close(menu_dialog)
            if on_delete_task:
                on_delete_task(task["id"])
        
        def handle_close(e):
            page.close(menu_dialog)
        
        menu_dialog = ft.AlertDialog(
            modal=False,
            title=ft.Text(f"Task: {task['title']}", size=16, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon("edit", color="#3b82f6"),
                    title=ft.Text("Edit Task"),
                    on_click=handle_edit
                ),
                ft.ListTile(
                    leading=ft.Icon("delete", color="#ef4444"),
                    title=ft.Text("Delete Task", color="#ef4444"),
                    on_click=handle_delete
                ),
            ], tight=True, spacing=0),
            actions=[
                ft.TextButton("Cancel", on_click=handle_close)
            ]
        )
        
        page.open(menu_dialog)
    
    return ft.Container(
        content=ft.Row([
            # Priority indicator
            ft.Container(
                width=4,
                height=40,
                bgcolor=get_priority_color(task["priority"]),
                border_radius=2
            ),
            
            # Task info
            ft.Column([
                ft.Text(task["title"], size=14, weight=ft.FontWeight.W_500, color="#1f2937"),
                ft.Row([
                    ft.Text(f"Priority: {task['priority'].capitalize()}", size=11, color="#6b7280"),
                    ft.Text("•", size=11, color="#6b7280"),
                    ft.Text(task.get("date", "No date"), size=11, color="#6b7280"),
                ], spacing=5)
            ], spacing=2, expand=True),
            
            # Status badge
            ft.Container(
                content=ft.Text(
                    task["status"].capitalize(), 
                    size=11, 
                    color="#ffffff",
                    weight=ft.FontWeight.W_500
                ),
                bgcolor=get_status_color(task["status"]),
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=12
            ),
            
            # More button - now with click handler
            ft.IconButton(
                icon="more_vert", 
                icon_size=18, 
                icon_color="#6b7280",
                on_click=show_task_menu
            )
        ], vertical_alignment="center", spacing=15),
        bgcolor="#ffffff",
        padding=15,
        border_radius=10,
        border=ft.border.all(1, "#e5e7eb"),
        data=task["id"]  # Store task ID in container for future reference
    )


def create_filter_handler(page, all_tasks_data, task_list_ref, current_filter, filter_buttons, filter_type, on_edit_task=None, on_delete_task=None):
    """
    Create filter handler function
    
    Args:
        page: Flet page object
        all_tasks_data: List of all tasks
        task_list_ref: Reference to task list column
        current_filter: Current filter state (list with one element)
        filter_buttons: Dictionary of filter button containers
        filter_type: Type of filter to apply
        on_edit_task: Callback for editing task
        on_delete_task: Callback for deleting task
    """
    def handler(e):
        current_filter[0] = filter_type
        
        # Update button styles
        for btn_type, btn in filter_buttons.items():
            if btn_type == filter_type:
                btn.bgcolor = "#e0e7ff"
                btn.content.color = "#6366f1"
                btn.content.weight = ft.FontWeight.W_500
            else:
                btn.bgcolor = "#f3f4f6"
                btn.content.color = "#6b7280"
                btn.content.weight = ft.FontWeight.NORMAL
        
        # Filter tasks
        if filter_type == "all":
            filtered = all_tasks_data
        else:
            filtered = [task for task in all_tasks_data if task["status"] == filter_type]
        
        # Update task list
        task_list_ref.current.controls.clear()
        
        if filtered:
            task_list_ref.current.controls.append(
                ft.Text(f"{len(filtered)} Tasks", size=14, color="#6b7280", weight=ft.FontWeight.W_500)
            )
            task_list_ref.current.controls.append(ft.Container(height=10))
            
            for task in filtered:
                task_list_ref.current.controls.append(
                    create_task_item(task, page, on_edit_task, on_delete_task)
                )
        else:
            task_list_ref.current.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon("inbox", size=48, color="#d1d5db"),
                        ft.Text("No tasks found", size=16, color="#6b7280"),
                    ], horizontal_alignment="center", spacing=10),
                    alignment=ft.alignment.center,
                    padding=40
                )
            )
        
        page.update()
    
    return handler