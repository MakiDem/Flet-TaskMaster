import flet as ft
from components.tasks_frame.task import create_task_item
from dialogs.edit_task_dialog import show_edit_task_dialog


def create_task_handlers(page, all_tasks_data, task_list_ref, current_filter, notif_manager):
    """
    Create all task handlers with shared state access.
    
    Returns:
        tuple: (handle_edit_task, handle_delete_task, refresh_task_list)
    """
    
    # Refresh task list
    def refresh_task_list():
        """Refresh the task list with current filter"""
        filter_type = current_filter[0]
        
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
                    create_task_item(task, page, handle_edit_task, handle_delete_task)
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
    
    # Edit task handler
    def handle_edit_task(task):
        """Handle edit button click"""
        def on_updated(updated_task):
            # Update task in list
            for i, t in enumerate(all_tasks_data):
                if t["id"] == updated_task["id"]:
                    all_tasks_data[i] = updated_task
                    break
            
            # Refresh display
            refresh_task_list()
            
            # Show notification
            if notif_manager:
                notif_manager.show("Task updated successfully!", "success", 3)
        
        show_edit_task_dialog(page, task, on_updated)
    
    # Delete task handler
    def handle_delete_task(task_id):
        """Handle delete button click"""
        def confirm_delete(e):
            page.close(confirm_dialog)
            
            # Remove task from list
            for i, t in enumerate(all_tasks_data):
                if t["id"] == task_id:
                    all_tasks_data.pop(i)
                    break
            
            # Refresh display
            refresh_task_list()
            
            # Show notification
            if notif_manager:
                notif_manager.show("Task deleted!", "info", 3)
        
        def cancel_delete(e):
            page.close(confirm_dialog)
        
        # Show confirmation dialog
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete Task?"),
            content=ft.Text("Are you sure you want to delete this task? This action cannot be undone."),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.ElevatedButton("Delete", on_click=confirm_delete, bgcolor="#ef4444", color="#ffffff"),
            ]
        )
        page.open(confirm_dialog)
    
    return handle_edit_task, handle_delete_task, refresh_task_list