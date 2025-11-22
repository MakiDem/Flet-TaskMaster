import flet as ft
from datetime import datetime
from components.sidebar import create_sidebar
from pages.dashboard import create_dashboard_page
from pages.all_tasks import create_all_tasks_page_content
from dialogs.add_task_dialog import show_add_task_dialog
from utils.check_overdue import check_overdue_tasks

from components.notification import NotificationManager


def main(page: ft.Page):
    page.title = "TaskMaster"
    page.window.width = 1440
    page.window.height = 800
    page.window.center()
    page.padding = 30
    page.bgcolor = "#f5f5f5"

    # Initialize notification manager
    notif_manager = NotificationManager(page)

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
    
    # References
    main_content_ref = ft.Ref[ft.Container]()
    sidebar_container = ft.Ref[ft.Container]()
    
    
    
    # Navigation handler
    def navigate_to(page_name):
        """Handle navigation between pages"""
        current_page[0] = page_name
        
        # Determine page content
        if page_name == "dashboard":
            page_content = create_dashboard_page(
                completed_tasks, pending_tasks, overdue_tasks, 
                completed_today, total_tasks, tasks_list
            )
            check_overdue_tasks(notif_manager, all_tasks_data)
        elif page_name == "all_tasks":
            page_content = create_all_tasks_page_content(
                page, all_tasks_data, lambda e: show_add_task_dialog(page, on_task_added), notif_manager=notif_manager
            )
        
        # Update main content - NO notification container needed
        main_content_ref.current.content = page_content
        
        # Update sidebar
        sidebar_container.current.content = create_sidebar(
            page, navigate_to, page_name, handle_add_task
        ).content
        
        page.update()
    
    # Callback when task is added
    def on_task_added(new_task):
        """Called when a new task is added from the dialog"""
        # Add task to list
        new_task["id"] = len(all_tasks_data) + 1
        if new_task.get("date") is None or new_task.get("date") == "":
            new_task["date"] = datetime.today().strftime("%b %d")
        else:
            new_task["date"] = new_task.get("due_date", datetime.today().strftime("%b %d"))
        all_tasks_data.append(new_task)
        
        # Refresh the all tasks page
        if current_page[0] == "all_tasks":
            navigate_to("all_tasks")
        
        # Show success notification
        notif_manager.show(
            "Task added successfully!",
            notification_type="success",
            duration=3
        )
    
    # Handle add task button click
    def handle_add_task(e):
        # Navigate to all tasks if not there
        if current_page[0] != "all_tasks":
            navigate_to("all_tasks")
        
        # Open the dialog
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
    
    # Check overdue tasks on startup
    check_overdue_tasks(notif_manager, all_tasks_data)

ft.app(target=main)