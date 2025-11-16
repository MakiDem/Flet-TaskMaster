import flet as ft

def create_stats(completed_tasks, pending_tasks, overdue_tasks):
    return ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Icon("check", color="#22c55e", size=30),
                ft.Text(str(completed_tasks), size=28, weight=ft.FontWeight.BOLD, color="#1f2937"),
                ft.Text("Completed", size=13, color="#6b7280")
            ], horizontal_alignment="center", spacing=5),
            bgcolor="#ffffff",
            padding=30,
            border_radius=15,
            expand=True,
            alignment=ft.alignment.center
        ),
        ft.Container(
            content=ft.Column([
                ft.Icon("schedule", color="#f59e0b", size=30),
                ft.Text(str(pending_tasks), size=28, weight=ft.FontWeight.BOLD, color="#1f2937"),
                ft.Text("Pending", size=13, color="#6b7280")
            ], horizontal_alignment="center", spacing=5),
            bgcolor="#ffffff",
            padding=30,
            border_radius=15,
            expand=True,
            alignment=ft.alignment.center
        ),
        ft.Container(
            content=ft.Column([
                ft.Icon("close", color="#ef4444", size=30),
                ft.Text(str(overdue_tasks), size=28, weight=ft.FontWeight.BOLD, color="#1f2937"),
                ft.Text("Overdue", size=13, color="#6b7280")
            ], horizontal_alignment="center", spacing=5),
            bgcolor="#ffffff",
            padding=30,
            border_radius=15,
            expand=True,
            alignment=ft.alignment.center
        )
    ], spacing=20)