import flet as ft
from utils.all_tasks_handlers import create_task_handlers
from utils.all_tasks_filters import create_filter_section
from utils.all_tasks_list_view import create_task_list_view
from utils.all_tasks_header import create_header
from utils.all_tasks_search_bar import create_search_bar

from database.crud import get_all_tasks

def create_all_tasks_page_content(page, all_tasks_data, show_add_dialog_handler, on_task_updated=None, on_task_deleted=None, notif_manager=None):
    """
    All Tasks page content
    
    Args:
        page: Flet page object
        all_tasks_data: List of all tasks
        show_add_dialog_handler: Function to show add dialog
        on_task_updated: Callback when task is updated
        on_task_deleted: Callback when task is deleted
        notif_manager: Notification manager for showing notifications
    """
    
    # Current filter state
    current_filter = ["all"]
    
    
    all_tasks_data.clear()
    all_tasks_data.extend(get_all_tasks())

    # References
    task_list_ref = ft.Ref[ft.Column]()
    filter_buttons = {}
    
    # Create handlers (passing all required references)
    handle_edit_task, handle_delete_task, refresh_task_list = create_task_handlers(
        page=page,
        all_tasks_data=all_tasks_data,
        task_list_ref=task_list_ref,
        current_filter=current_filter,
        notif_manager=notif_manager
    )
    
    # Create filter section
    filter_row, filter_buttons = create_filter_section(
        page=page,
        all_tasks_data=all_tasks_data,
        task_list_ref=task_list_ref,
        current_filter=current_filter,
        handle_edit_task=handle_edit_task,
        handle_delete_task=handle_delete_task
    )
    
    # Create initial task list
    initial_tasks = create_task_list_view(
        task_list_ref=task_list_ref,
        all_tasks_data=all_tasks_data,
        page=page,
        handle_edit_task=handle_edit_task,
        handle_delete_task=handle_delete_task
    )
    
    # Return page content
    return ft.Column([
        # Header
        create_header(show_add_dialog_handler),
        
        ft.Container(height=20),
        
        # Search and filter
        create_search_bar(),
        
        ft.Container(height=20),
        
        # Filter tabs
        filter_row,
        
        ft.Container(height=20),
        
        # Task list
        initial_tasks
    ], scroll="auto")