import flet as ft

def create_all_tasks_page(page):
    """All Tasks page with filtering and add task dialog"""
    
    # Task data
    all_tasks_data = [
        {"id": 1, "title": "Complete project proposal", "status": "completed", "priority": "high", "date": "Nov 16"},
        {"id": 2, "title": "Review code changes", "status": "pending", "priority": "medium", "date": "Nov 17"},
        {"id": 3, "title": "Update documentation", "status": "overdue", "priority": "low", "date": "Nov 15"},
        {"id": 4, "title": "Team meeting at 3 PM", "status": "pending", "priority": "high", "date": "Nov 16"},
        {"id": 5, "title": "Fix bug in login page", "status": "completed", "priority": "high", "date": "Nov 14"},
        {"id": 6, "title": "Design new landing page", "status": "pending", "priority": "medium", "date": "Nov 18"},
        {"id": 7, "title": "Write unit tests", "status": "overdue", "priority": "high", "date": "Nov 13"},
    ]
    
    # Current filter state
    current_filter = ["all"]  # Use list to modify in nested functions
    
    # References
    task_list_ref = ft.Ref[ft.Column]()
    filter_buttons = {}
    
    def get_priority_color(priority):
        colors = {
            "high": "#ef4444",
            "medium": "#f59e0b",
            "low": "#22c55e"
        }
        return colors.get(priority, "#6b7280")
    
    def get_status_color(status):
        colors = {
            "completed": "#22c55e",
            "pending": "#f59e0b",
            "overdue": "#ef4444"
        }
        return colors.get(status, "#6b7280")
    
    def create_task_item(task):
        """Create a single task item"""
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
                        ft.Text(task["date"], size=11, color="#6b7280"),
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
                
                # More button
                ft.IconButton(icon="more_vert", icon_size=18, icon_color="#6b7280")
            ], vertical_alignment="center", spacing=15),
            bgcolor="#ffffff",
            padding=15,
            border_radius=10,
            border=ft.border.all(1, "#e5e7eb")
        )
    
    def filter_tasks(filter_type):
        """Filter tasks based on status"""
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
                    task_list_ref.current.controls.append(create_task_item(task))
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
    
    def show_add_task_dialog(e):
        """Show dialog to add new task"""
        
        # Input fields
        title_field = ft.TextField(
            label="Task Title",
            hint_text="Enter task title",
            autofocus=True,
            width=500
        )
        
        description_field = ft.TextField(
            label="Description",
            hint_text="Enter task description",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=500
        )
        
        priority_dropdown = ft.Dropdown(
            label="Priority",
            width=500,
            options=[
                ft.dropdown.Option("high", "High"),
                ft.dropdown.Option("medium", "Medium"),
                ft.dropdown.Option("low", "Low"),
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
            width=500,
            value="Nov 16"
        )
        
        error_text = ft.Text("", color="#ef4444", size=12)
        
        def save_task(e):
            """Save the task"""
            if not title_field.value or title_field.value.strip() == "":
                error_text.value = "Title is required!"
                page.update()
                return
            
            # Add task to list
            new_task = {
                "id": len(all_tasks_data) + 1,
                "title": title_field.value.strip(),
                "status": status_dropdown.value,
                "priority": priority_dropdown.value,
                "date": due_date_field.value
            }
            all_tasks_data.append(new_task)
            
            # Close dialog
            dialog.open = False
            page.update()
            
            # Refresh task list
            filter_tasks(current_filter[0])(None)
            
            # Show success message
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Task added successfully!"),
                bgcolor="#22c55e"
            )
            page.snack_bar.open = True
            page.update()
        
        def cancel(e):
            dialog.open = False
            page.update()
        
        # Create dialog
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon("add_task", color="#6366f1", size=24),
                ft.Text("Add New Task", size=20, weight=ft.FontWeight.BOLD)
            ], spacing=10),
            content=ft.Container(
                content=ft.Column([
                    title_field,
                    description_field,
                    priority_dropdown,
                    status_dropdown,
                    due_date_field,
                    error_text
                ], tight=True, spacing=15),
                width=500,
                padding=10
            ),
            actions=[
                ft.TextButton("Cancel", on_click=cancel),
                ft.ElevatedButton("Save Task", on_click=save_task, bgcolor="#6366f1", color="#ffffff"),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    # Create filter buttons
    all_btn = ft.Container(
        content=ft.Text("All", size=13, color="#6366f1", weight=ft.FontWeight.W_500),
        bgcolor="#e0e7ff",
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=6,
        on_click=filter_tasks("all"),
        ink=True
    )
    
    completed_btn = ft.Container(
        content=ft.Text("Completed", size=13, color="#6b7280"),
        bgcolor="#f3f4f6",
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=6,
        on_click=filter_tasks("completed"),
        ink=True
    )
    
    pending_btn = ft.Container(
        content=ft.Text("Pending", size=13, color="#6b7280"),
        bgcolor="#f3f4f6",
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=6,
        on_click=filter_tasks("pending"),
        ink=True
    )
    
    overdue_btn = ft.Container(
        content=ft.Text("Overdue", size=13, color="#6b7280"),
        bgcolor="#f3f4f6",
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=6,
        on_click=filter_tasks("overdue"),
        ink=True
    )
    
    filter_buttons = {
        "all": all_btn,
        "completed": completed_btn,
        "pending": pending_btn,
        "overdue": overdue_btn
    }
    
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
                on_click=show_add_task_dialog
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