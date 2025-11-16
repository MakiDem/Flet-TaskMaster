import flet as ft

def create_time():
    return ft.Container(
        content=ft.Column([
            ft.Text("Time", size=12, color="#6b7280", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Text("09:41", size=24, weight=ft.FontWeight.BOLD, color="#1f2937"),
                ft.Container(
                    content=ft.Text("AM", size=10, color="#6b7280"),
                    bgcolor="#f3f4f6",
                    padding=5,
                    border_radius=5
                ),
                ft.Container(
                    content=ft.Text("PM", size=10, color="#6b7280"),
                    bgcolor="#ffffff",
                    padding=5,
                    border_radius=5,
                    border=ft.border.all(1, "#e5e7eb")
                )
            ], spacing=10)
        ], spacing=10)
    )