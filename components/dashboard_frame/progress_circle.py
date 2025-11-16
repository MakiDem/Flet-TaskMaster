import flet as ft

def create_progress_circle(completed_today=0, total_tasks=1):
        progress = completed_today / total_tasks
        
        return ft.Stack([
            ft.Container(
                width=180,
                height=180,
                border_radius=90,
                bgcolor="#e0e7ff"
            ),
            ft.Container(
                width=180,
                height=180,
                border_radius=90,
                gradient=ft.SweepGradient(
                    center=ft.alignment.center,
                    colors=["#7c3aed", "#a78bfa", "#e0e7ff"],
                    stops=[0, progress, progress]
                )
            ),
            ft.Container(
                width=120,
                height=120,
                border_radius=60,
                bgcolor="#f5f5f5",
                left=30,
                top=30
            )
        ])