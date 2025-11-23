import flet as ft
from components.dashboard_frame.progress_circle import create_progress_circle

def create_progress_card(completed_today, total_tasks):
    if total_tasks == 0:
        return ft.Container(
            width=350,
            height=250,
            content=ft.Text("No tasks for today!", size=16, color="#6b7280", weight=ft.FontWeight.W_500),
            alignment=ft.alignment.center,
            bgcolor="#ffffff",
            padding=30,
            border_radius=15,
        )
    else:
        return ft.Container(
            content=ft.Column([
                create_progress_circle(completed_today=completed_today, total_tasks=total_tasks),
                ft.Container(height=20),
                ft.Text("Progress For Today", size=18, weight=ft.FontWeight.BOLD, color="#1f2937"),
                ft.Text(f"{completed_today}/{total_tasks} Tasks Completed", size=14, color="#6b7280")
            ], horizontal_alignment="center"),
            bgcolor="#ffffff",
            padding=30,
            border_radius=15,
            width=350,
            alignment=ft.alignment.center
    )