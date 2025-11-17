import flet as ft
from datetime import datetime
from components.sidebar import create_sidebar
from pages.dashboard import create_dashboard_page
from pages.all_tasks import create_all_tasks_page_content
from dialogs.add_task_dialog import show_add_task_dialog


def main(page: ft.Page):
    page.title = "TaskMaster"
    page.window.width = 1440
    page.window.height = 800
    page.window.center()
    page.padding = 30
    page.bgcolor = "#f5f5f5"

    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),
        bgcolor="#22c55e",
        duration=3000
    )

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

    completed_tasks = 10
    pending_tasks = 10
    overdue_tasks = 10
    total_tasks = 11
    completed_today = 9

    tasks_list = [
        {"name": "Task", "completed": True},
        {"name": "Task", "completed": True},
        {"name": "Task", "completed": False},
    ]
    
    # Current page state
    current_page = ["dashboard"]
    
    # Flag to track if task was just added
    task_just_added = [False]
    
    # References
    main_content_ref = ft.Ref[ft.Container]()
    sidebar_container = ft.Ref[ft.Container]()
    
    # Navigation handler - DEFINE THIS FIRST
    def navigate_to(page_name):
        """Handle navigation between pages"""
        print(f"Navigating to: {page_name}")
        current_page[0] = page_name
        
        # Update main content based on selected page
        if page_name == "dashboard":
            main_content_ref.current.content = create_dashboard_page(
                completed_tasks, pending_tasks, overdue_tasks, 
                completed_today, total_tasks, tasks_list
            )
        elif page_name == "all_tasks":
            # Pass the dialog opener and task data
            main_content_ref.current.content = create_all_tasks_page_content(
                page, all_tasks_data, lambda e: show_add_task_dialog(page, on_task_added)
            )
        
        # Update sidebar to show active state
        sidebar_container.current.content = create_sidebar(
            page, navigate_to, page_name, handle_add_task
        ).content
        
        
        
        # Show snackbar AFTER page.update() if task was just added
        if task_just_added[0] and page_name == "all_tasks":
            task_just_added[0] = False  # Reset flag
            page.snack_bar.content = ft.Text("✅ Task added successfully!")
            page.snack_bar.open = True
            page.update()
        
        page.update()

    
    # Callback when task is added - DEFINE AFTER navigate_to
    def on_task_added(new_task):
        """Called when a new task is added from the dialog"""
        print(f"Task added: {new_task}")
        
        # Add task to list
        new_task["id"] = len(all_tasks_data) + 1
        new_task["date"] = new_task.get("due_date", datetime.today().strftime("%b %d"))
        all_tasks_data.append(new_task)
        
        # Set flag
        task_just_added[0] = True
        
        # Refresh the all tasks page
        if current_page[0] == "all_tasks":
            navigate_to("all_tasks")
    
    # Handle add task button click - DEFINE AFTER on_task_added
    def handle_add_task(e):
        print("Add task button clicked!")
        
        # Navigate to all tasks if not there
        if current_page[0] != "all_tasks":
            print("Navigating to all tasks...")
            navigate_to("all_tasks")
        
        # Open the dialog
        print("Opening dialog...")
        show_add_task_dialog(page, on_task_added)
    
    # Create sidebar
    sidebar = ft.Container(
        ref=sidebar_container,
        content=create_sidebar(page, navigate_to, "dashboard", handle_add_task).content
    )

    # Create main content (starts with dashboard)
    main_content = ft.Container(
        ref=main_content_ref,
        expand=True,
        content=create_dashboard_page(
            completed_tasks, pending_tasks, overdue_tasks,
            completed_today, total_tasks, tasks_list
        ),
        bgcolor="#f3f4f6",
        padding=25,
        border_radius=15,
    )

    # Layout
    page.add(
        ft.Row([sidebar, main_content], spacing=0, expand=True)
    )

ft.app(target=main)