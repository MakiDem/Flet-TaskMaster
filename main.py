import flet as ft
from datetime import datetime
from components.sidebar import create_sidebar
from components.dashboard_frame.progress_circle import create_progress_circle
from components.dashboard_frame.stat_cards import create_stats
from components.searchbar import create_searchbar
from components.dashboard_frame.progress_card import create_progress_card


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
        padding=30,
        bgcolor="#f9fafb",
        content=ft.Column([
            # Search bar
            create_searchbar(),
            
            ft.Container(height=20),
            
            # Stats cards
            create_stats(completed_tasks=completed_tasks, pending_tasks=pending_tasks, overdue_tasks=overdue_tasks),
            
            ft.Container(height=20),
            
            # Today's Tasks and Progress
            ft.Row([
                # Today's Tasks Card
                ft.Container(
                    content=ft.Column([
                        ft.Text("Today's Tasks", size=18, weight=ft.FontWeight.BOLD, color="#1f2937"),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Text(
                                '"You don\'t have to be great to start, but you have to start to be great." – Zig Ziglar',
                                size=12,
                                color="#6b7280",
                                italic=True
                            ),
                            padding=10,
                            bgcolor="#fef3c7",
                            border_radius=8
                        ),
                        ft.Container(height=15),
                        ft.Column([
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Task", size=14, color="#1f2937"),
                                    ft.Container(expand=True),
                                    ft.Checkbox(value=True, fill_color="#6366f1")
                                ]),
                                bgcolor="#e0e7ff",
                                padding=12,
                                border_radius=8
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Task", size=14, color="#1f2937"),
                                    ft.Container(expand=True),
                                    ft.Checkbox(value=True, fill_color="#6366f1")
                                ]),
                                bgcolor="#e0e7ff",
                                padding=12,
                                border_radius=8
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Task", size=14, color="#1f2937"),
                                    ft.Container(expand=True),
                                    ft.Checkbox(value=False, fill_color="#6366f1")
                                ]),
                                bgcolor="#e0e7ff",
                                padding=12,
                                border_radius=8
                            )
                        ], spacing=10)
                    ]),
                    bgcolor="#f3f4f6",
                    padding=25,
                    border_radius=15,
                    expand=True
                ),
                
                # Progress Card
                create_progress_card(completed_today, total_tasks)
            ], spacing=20, expand=True)
        ])
    )
    
    # Layout
    page.add(
        ft.Row([
            sidebar,
            main_content
        ], spacing=0, expand=True)
    )

ft.app(target=main)