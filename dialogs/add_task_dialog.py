from datetime import timedelta
import datetime
import flet as ft

def show_add_task_dialog(page, on_task_added=None):
    """
    Show dialog to add new task
    
    Args:
        page: Flet page object
        on_task_added: Callback function to call after task is added
    """
    
    print(f"=== show_add_task_dialog called ===")
    
    try:
        def save_task(e):
            """Validate and save the task"""
            print("save_task called")
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
                "due_date": due_date_field.value.strip() if due_date_field.value else (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                "category": category_dropdown.value
            }
            
            # Close dialog first using page.close(dialog) (reliable pattern)
            try:
                page.close(dialog)
            except Exception:
                try:
                    dialog.open = False
                    page.update()
                except Exception:
                    pass

            
            if on_task_added:
                on_task_added(new_task)
            page.update()
        
        def cancel(e):
            """Close dialog without saving"""
            print("cancel called")
            page.close(dialog)
        
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
        
        # Create dialog
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon("add_task", color="#6366f1", size=28),
                ft.Text("Add New Task", size=20, weight=ft.FontWeight.BOLD, color="#cacaca")
            ], spacing=10),
            content=ft.Container(
                content=ft.Column([
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
                    "Save Task", 
                    on_click=save_task, 
                    bgcolor="#6366f1", 
                    color="#ffffff",
                    icon="check"
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
    # Open the dialog using page.open (restores previous working pattern)
        page.open(dialog)
        print("Dialog opened via page.open(dialog)")

    except Exception as e:
        print(f"ERROR in show_add_task_dialog: {e}")
        import traceback
        traceback.print_exc()