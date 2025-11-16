import flet as ft
from components.calendar import create_calendar
from components.time import create_time
from components.add_btn import create_addbtn

def create_sidebar(page: ft.Page, on_navigate, current_page="dashboard"):
    """
    Create sidebar with navigation
    
    Args:
        on_navigate: callback function to handle navigation
        current_page: which page is currently active ("dashboard" or "all_tasks")
    """
    
    return ft.Container(
        width=280,
        bgcolor="#ffffff",
        padding=ft.padding.only(left=20, right=20, top=30, bottom=30),
        content=ft.Column([
            # Logo
            ft.Row([
                ft.Image(
                    width=50,
                    height=50,
                    src="assets/logo.png"
                ),
                ft.Text("TaskMaster", size=24, weight=ft.FontWeight.BOLD, color="#2913D0")
            ], spacing=15),
            
            ft.Container(height=30),
            
            # Navigation - Dashboard
            ft.Container(
                content=ft.Text(
                    "Dashboard", 
                    size=14, 
                    color="#1f2937" if current_page == "dashboard" else "#6b7280"
                ),
                bgcolor="#f3f4f6" if current_page == "dashboard" else "transparent",
                padding=15,
                border_radius=8,
                on_click=lambda e: on_navigate("dashboard"),
                ink=True
            ),
            
            # Navigation - All Tasks
            ft.Container(
                content=ft.Text(
                    "All Tasks", 
                    size=14, 
                    color="#1f2937" if current_page == "all_tasks" else "#6b7280"
                ),
                bgcolor="#f3f4f6" if current_page == "all_tasks" else "transparent",
                padding=15,
                border_radius=8,
                on_click=lambda e: on_navigate("all_tasks"),
                ink=True
            ),
            
            ft.Container(height=20),
            
            # Calendar
            create_calendar(),
            
            ft.Container(height=20),
            
            # Time
            create_time(),
            
            ft.Container(expand=True),
            
            # Create add Button - Pass page object here
            create_addbtn(page)
        ])
    )