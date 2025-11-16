import flet as ft

def show_add_task_dialog(page, on_task_added=None):
    """
    Show dialog to add new task
    
    Args:
        page: Flet page object
        on_task_added: Callback function to call after task is added
    """
    
    # Input fields
    title_field = ft.TextField(
        label="Task Title",
        hint_text="Enter task title",
        autofocus=True,
        width=500
    )
    
    description_field = ft.TextField(
        label="Description",
        hint_text="Enter task description (optional)",
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
        value="medium"
    )
    
    status_dropdown = ft.Dropdown(
        label="Status",
        width=500,
        options=[
            ft.dropdown.Option("pending", "Pending"),
            ft.dropdown.Option("completed", "Completed"),
            ft.dropdown.Option("overdue", "Overdue"),
        ],
        value="pending"
    )
    
    due_date_field = ft.TextField(
        label="Due Date",
        hint_text="YYYY-MM-DD",
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
        value="work"
    )
    
    error_text = ft.Text("", color="#ef4444", size=12)
    
    def save_task(e):
        """Validate and save the task"""
        if not title_field.value or title_field.value.strip() == "":
            error_text.value = "⚠️ Title is required!"
            page.update()
            return
        
        # Create task object
        new_task = {
            "title": title_field.value.strip(),
            "description": description_field.value.strip() if description_field.value else "",
            "priority": priority_dropdown.value,
            "status": status_dropdown.value,
            "due_date": due_date_field.value.strip() if due_date_field.value else "",
            "category": category_dropdown.value
        }
        
        # Close dialog
        dialog.open = False
        page.update()
        
        # Call callback if provided
        if on_task_added:
            on_task_added(new_task)
        
        # Show success message
        page.snack_bar = ft.SnackBar(
            content=ft.Text("✅ Task added successfully!"),
            bgcolor="#22c55e"
        )
        page.snack_bar.open = True
        page.update()
    
    def cancel(e):
        """Close dialog without saving"""
        dialog.open = False
        page.update()
    
    # Create dialog
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon("add_task", color="#6366f1", size=28),
            ft.Text("Add New Task", size=20, weight=ft.FontWeight.BOLD, color="#1f2937")
        ], spacing=10),
        content=ft.Container(
            content=ft.Column([
                title_field,
                description_field,
                ft.Row([
                    priority_dropdown,
                ], spacing=10),
                ft.Row([
                    status_dropdown,
                ], spacing=10),
                due_date_field,
                category_dropdown,
                error_text
            ], tight=True, spacing=15, scroll="auto"),
            width=500,
            height=500,  # Max height for scrolling
            padding=10
        ),
        actions=[
            ft.TextButton("Cancel", on_click=cancel),
            ft.ElevatedButton(
                "Save Task", 
                on_click=save_task, 
                bgcolor="#6366f1", 
                color="#ffffff",
                icon="check"
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()