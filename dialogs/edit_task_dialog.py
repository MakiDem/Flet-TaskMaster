import datetime
import flet as ft

def validate_date(date_string):
    """
    Simple date validation: checks format and ensures date is today or future
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not date_string or date_string.strip() == "":
        return False, "Date is required"
    
    try:
        # Parse the date
        parsed_date = datetime.datetime.strptime(date_string.strip(), "%Y-%m-%d")
        
        # Check if date is today or in the future
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if parsed_date < today:
            return False, "Date must be today or in the future"
        
        return True, ""
    
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD (e.g., 2024-12-31)"


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
        hint_text="YYYY-MM-DD (e.g., 2024-12-31)",
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
    
    error_text = ft.Text("", color="#ef4444", size=12, weight=ft.FontWeight.W_500)
    
    def save_task(e):
        """Validate and save the updated task"""
        
        # Reset error
        error_text.value = ""
        
        # Validate title
        if not title_field.value or title_field.value.strip() == "":
            error_text.value = "⚠️ Title is required!"
            page.update()
            return
        
        # Validate date
        date_value = due_date_field.value.strip() if due_date_field.value else ""
        if date_value:  # Only validate if a date is provided
            is_valid, error_msg = validate_date(date_value)
            if not is_valid:
                error_text.value = f"⚠️ {error_msg}"
                page.update()
                return
        
        # Create updated task object (keep the same ID)
        updated_task = {
            "id": task["id"],  # Keep original ID
            "title": title_field.value.strip(),
            "description": description_field.value.strip() if description_field.value else "",
            "priority": priority_dropdown.value,
            "status": status_dropdown.value,
            "due_date": date_value,
            "category": category_dropdown.value
        }
        
        # Close dialog
        page.close(dialog)
        
        # Call callback if provided (direct, with simple error logging).
        if on_task_updated:
            try:
                on_task_updated(updated_task)
            except Exception as e:
                import traceback
                print(f"ERROR in on_task_updated: {e}")
                print("Updated task payload:", updated_task)
                traceback.print_exc()
    
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