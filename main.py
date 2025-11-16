import flet as ft
from datetime import datetime
from components.sidebar import create_sidebar
from components.dashboard_frame.progress_circle import create_progress_circle
from components.dashboard_frame.stat_cards import create_stats
from components.searchbar import create_searchbar
from components.dashboard_frame.today import render_today_section


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

    # Progress circle (donut chart simulation)
    create_progress_circle()

    # Sidebar
    sidebar = create_sidebar()

    # Main content
    main_content = ft.Container(
        expand=True,
        content=ft.Column(
            [
                # Search bar
                create_searchbar(),
                ft.Container(height=20),
                # Stats cards
                create_stats(
                    completed_tasks=completed_tasks,
                    pending_tasks=pending_tasks,
                    overdue_tasks=overdue_tasks,
                ),
                ft.Container(height=20),
                # Today's Tasks and Progress
                render_today_section(completed_today, total_tasks, tasks_list)
            ]
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