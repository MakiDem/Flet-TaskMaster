import flet as ft

from components.task_card import create_taskcard
from components.dashboard_frame.progress_card import create_progress_card

def render_today_section(completed_tasks, total_tasks, tasks_list):
    return ft.Row(
        [
            # Today's Tasks Card
            ft.Container(
            content=ft.Column([
                ft.Text("Today's Tasks", size=18, weight=ft.FontWeight.BOLD, color="#1f2937"),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Text(
                        "You don't have to be great to start, but you have to start to be great. – Zig Ziglar",
                        size=12,
                        color="#6b7280",
                        italic=True,
                    ),
                    padding=10,
                    bgcolor="#fef3c7",
                    border_radius=8,
                ),
                ft.Container(height=15),
                ft.Column([
                    create_taskcard("Short task", True),
                    create_taskcard("This is a very long task that wraps", True),
                    create_taskcard("Another task", False),
                ], spacing=10),
            ]),
                bgcolor="#f3f4f6",  # Changed background
                padding=25,
                border_radius=15,
                expand=True  # THIS IS KEY - makes container take full width
            ),
            # Progress Card
            create_progress_card(completed_tasks, total_tasks),
        ],
        spacing=20,
        expand=True,
    )