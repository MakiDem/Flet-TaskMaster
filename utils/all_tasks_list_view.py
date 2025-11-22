import flet as ft
from components.tasks_frame.task import create_task_item


def create_task_list_view(task_list_ref, all_tasks_data, page, handle_edit_task, handle_delete_task):
    """
    Create and populate the initial task list.
    
    Args:
        task_list_ref: Reference to task list Column
        all_tasks_data: List of all tasks
        page: Flet page object
        handle_edit_task: Edit task handler function
        handle_delete_task: Delete task handler function
    
    Returns:
        ft.Column: Populated task list column
    """
    
    # Initial task list
    initial_tasks = ft.Column(ref=task_list_ref, spacing=10, scroll="auto")
    
    # Populate initial tasks
    initial_tasks.controls.append(
        ft.Text(f"{len(all_tasks_data)} Tasks", size=14, color="#6b7280", weight=ft.FontWeight.W_500)
    )
    initial_tasks.controls.append(ft.Container(height=10))
    
    for task in all_tasks_data:
        initial_tasks.controls.append(
            create_task_item(task, page, handle_edit_task, handle_delete_task)
        )
    
    return initial_tasks