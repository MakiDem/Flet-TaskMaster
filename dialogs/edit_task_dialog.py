import flet as ft

def show_edit_task_dialog(page, task, on_task_updated=None):
    """
    Show dialog to edit an existing task
    
    Args:
        page: Flet page object
        task: Task dictionary to edit (must include 'id')
        on_task_updated: Callback function after task is updated
    """
    
    print(f"Editing task ID: {task['id']}")
    
    # Input fields - pre-populated with existing task data
    title_field = ft.TextField(
        label="Task Title",
        value=task.get("title", ""),
        autofocus=True,
        width=500
    )
    
    description_field = ft.TextField(
        label="Description",
        value=task.get("description", ""),
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=500
    )
    
    priority_dropdown = ft.Dropdown(
        label="Priority Level",
        width=500,
        options=[
            ft.dropdown.Option("high", "High Priority"),
            ft.dropdown.Option("medium", "Medium Priority"),
            ft.dropdown.Option("low", "Low Priority"),
        ],
        value=task.get("priority", "medium")
    )
    
    status_dropdown = ft.Dropdown(
        label="Status",
        width=500,
        options=[
            ft.dropdown.Option("pending", "Pending"),
            ft.dropdown.Option("completed", "Completed"),
            ft.dropdown.Option("overdue", "Overdue"),
        ],
        value=task.get("status", "pending")
    )
    
    due_date_field = ft.TextField(
        label="Due Date",
        value=task.get("date", task.get("due_date", "")),
        width=500
    )
    
    category_dropdown = ft.Dropdown(
        label="Category",
        width=500,
        options=[
            ft.dropdown.Option("work", "Work"),
            ft.dropdown.Option("personal", "Personal"),
            ft.dropdown.Option("study", "Study"),
            ft.dropdown.Option("other", "Other"),
        ],
        value=task.get("category", "work")
    )
    
    error_text = ft.Text("", color="#ef4444", size=12)
    
    def save_task(e):
        """Validate and save the updated task"""
        if not title_field.value or title_field.value.strip() == "":
            error_text.value = "⚠️ Title is required!"
            page.update()
            return
        
        # Create updated task object (keep the same ID)
        updated_task = {
            "id": task["id"],  # Keep original ID
            "title": title_field.value.strip(),
            "description": description_field.value.strip() if description_field.value else "",
            "priority": priority_dropdown.value,
            "status": status_dropdown.value,
            "due_date": due_date_field.value.strip() if due_date_field.value else "",
            "category": category_dropdown.value
        }
        
        # Close dialog
        page.close(dialog)
        
        # Call callback if provided
        if on_task_updated:
            on_task_updated(updated_task)
    
    def cancel(e):
        """Close dialog without saving"""
        page.close(dialog)
    
    # Create dialog
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon("edit", color="#6098ff", size=28),
            ft.Text("Edit Task", size=20, weight=ft.FontWeight.BOLD, color="#ffffff")
        ], spacing=10),
        content=ft.Container(
            content=ft.Column([
                ft.Text(f"Task ID: {task['id']}", size=12, color="#9ca3af"),
                title_field,
                description_field,
                priority_dropdown,
                status_dropdown,
                due_date_field,
                category_dropdown,
                error_text
            ], tight=True, spacing=15, scroll="auto"),
            width=500,
            height=500,
            padding=10
        ),
        actions=[
            ft.TextButton("Cancel", on_click=cancel),
            ft.ElevatedButton(
                "Save Changes", 
                on_click=save_task, 
                bgcolor="#3b82f6", 
                color="#ffffff",
                icon="save"
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    
    page.open(dialog)