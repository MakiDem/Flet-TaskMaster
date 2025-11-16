import flet as ft
from datetime import datetime
from components.sidebar import create_sidebar
from pages.dashboard import create_dashboard_page
from pages.all_tasks import create_all_tasks_page


def main(page: ft.Page):
    page.title = "TaskMaster"
    page.window.width = 1440
    page.window.height = 800
    page.window.center()
    page.padding = 30
    page.bgcolor = "#f5f5f5"

    # Task data
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
        
        # Update main content based on selected page
        if page_name == "dashboard":
            main_content_ref.current.content = create_dashboard_page(
                completed_tasks, pending_tasks, overdue_tasks, 
                completed_today, total_tasks, tasks_list
            )
        elif page_name == "all_tasks":
            main_content_ref.current.content = create_all_tasks_page(page)
        
        # Update sidebar to show active state
        sidebar_container.current.content = create_sidebar(
            page,           # Pass page object
            navigate_to,    # Pass navigate function
            page_name       # Pass current page name
        ).content
        
        page.update()
    
    # Create sidebar - IMPORTANT: Pass page, navigate_to function, and current page
    sidebar = ft.Container(
        ref=sidebar_container,
        content=create_sidebar(page, navigate_to, "dashboard").content
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