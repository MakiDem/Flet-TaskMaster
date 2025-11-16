# Sidebar
import flet as ft
from components.calendar import create_calendar
from components.time import create_time
from components.add_btn import create_addbtn

def create_sidebar():
    return ft.Container(
        width=280,
        bgcolor="#ffffff",
        padding=ft.padding.only(left=20, right=60, top=30, bottom=30),
        content=ft.Column([
            # Logo
            ft.Row([
                ft.Image(
                    width=50,
                    height=50,
                    src = "assets/logo.png"
                ),
                ft.Text("TaskMaster", size=24, weight=ft.FontWeight.BOLD, color="#1f2937")
            ], spacing=15),
            
            ft.Container(height=30),
            
            # Navigation
            ft.Container(
                content=ft.Text("Dashboard", size=14, color="#1f2937"),
                bgcolor="#f3f4f6",
                padding=15,
                border_radius=8
            ),
            ft.Container(
                content=ft.Text("All Tasks", size=14, color="#6b7280"),
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=20),
            
            # Calendar
            create_calendar(),
            
            ft.Container(height=20),
            
            # Time
            create_time(),
            
            ft.Container(expand=True),
            
            # Create add Button
            create_addbtn()
        ])
    )