import flet as ft
from components.calendar import create_calendar
from components.time import create_time
from components.add_btn import create_addbtn

def create_sidebar(page, on_navigate, current_page, on_add_task):
    """
    Create sidebar with navigation
    
    Args:
        page: Flet page object
        on_navigate: callback function to handle navigation
        current_page: which page is currently active
        on_add_task: callback function to handle add task button click
    """
    
    return ft.Container(
        width=280,
        bgcolor="#ffffff",
        padding=ft.padding.only(left=20, right=20, top=30, bottom=30),
        content=ft.Column([
            # Logo
            ft.Row([
                ft.Container(
                    width=50,
                    height=50,
                    bgcolor="#6366f1",
                    border_radius=25,
                    content=ft.Icon("check", color="#ffffff", size=30),
                    alignment=ft.alignment.center
                ),
                ft.Text("TaskMaster", size=24, weight=ft.FontWeight.BOLD, color="#1f2937")
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
            
            # Create add Button
            create_addbtn(page, on_add_task)
        ])
    )