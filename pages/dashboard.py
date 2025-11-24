import flet as ft
from components.searchbar import create_searchbar
from database.crud import search_tasks
from components.dashboard_frame.stat_cards import create_stats
from components.dashboard_frame.today import render_today_section
from dialogs.add_task_dialog import show_add_task_dialog
from dialogs.edit_task_dialog import show_edit_task_dialog
from utils.all_tasks_handlers import update_task

def create_dashboard_page(page, completed_tasks, pending_tasks, overdue_tasks, completed_today, total_tasks, tasks_list, notif_manager=None, refresh_task_list=None):
    """
    Create the dashboard page content.
    
    Args:
        page: Flet page object (REQUIRED for dialogs and searchbar)
        completed_tasks: Number of completed tasks
        pending_tasks: Number of pending tasks
        overdue_tasks: Number of overdue tasks
        completed_today: Number of tasks completed today
        total_tasks: Total number of tasks
        tasks_list: List of all tasks
    """
    
    def handle_edit_task(task):
        """Wrapper to handle task editing from search."""
        """Handle edit button click"""

        all_tasks_data = tasks_list
        def on_updated(updated_task):
            # Update task in list
            # Defensive: ensure payload is a dict and has 'id'
            if not isinstance(updated_task, dict) or "id" not in updated_task:
                print("all_tasks_handlers.on_updated received unexpected payload:", updated_task)
                return

            
            # Update DB record using allowed fields
            update_task(updated_task["id"], **{k: v for k, v in updated_task.items() if k != "id"})
            
            
            # Refresh display
            refresh_task_list()
            
            # Show notification
            if notif_manager:
                notif_manager.show("Task updated successfully!", "success", 3)
        
        show_edit_task_dialog(page, task, on_updated)
    
    def handle_add_task(e=None):
        """Wrapper to handle adding new task."""
        def on_added(new_task):
            # Add task to tasks_list
            tasks_list.append(new_task)
            
            # Refresh the page
            page.update()
            print(f"Task added: {new_task['title']}")
        
        show_add_task_dialog(page, on_task_added=on_added)
    
    return ft.Column([
        # Search bar
        create_searchbar(
            page=page,
            all_tasks_data=tasks_list,
            on_task_click=handle_edit_task,
            show_add_dialog_handler=handle_add_task,
            db_search_fn=search_tasks
        ),
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
    ], scroll="auto")