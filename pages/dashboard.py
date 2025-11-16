import flet as ft
from components.searchbar import create_searchbar
from components.dashboard_frame.stat_cards import create_stats
from components.dashboard_frame.today import render_today_section

def create_dashboard_page(completed_tasks, pending_tasks, overdue_tasks, completed_today, total_tasks, tasks_list):
    """
    Create the dashboard page content
    This is what was previously in main_content
    """
    return ft.Column([
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
    ])