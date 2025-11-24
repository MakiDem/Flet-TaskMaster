import flet as ft


def create_searchbar(page, all_tasks_data=None, on_task_click=None, show_add_dialog_handler=None, db_search_fn=None):
    """
    Create a searchbar with dropdown for task search.
    
    Args:
        page: Flet page object
        all_tasks_data: List of all tasks
        on_task_click: Callback when task is clicked (opens edit dialog)
        show_add_dialog_handler: Function to show add dialog
    
    Returns:
        ft.Container: Searchbar component
    """
    
    # References
    search_field_ref = ft.Ref[ft.TextField]()
    dropdown_ref = ft.Ref[ft.Column]()
    dropdown_container_ref = ft.Ref[ft.Container]()
    
    def filter_tasks(search_query):
        """Filter tasks based on search query.

        Uses `db_search_fn` if provided (queries DB), otherwise falls back to
        in-memory `all_tasks_data` list.
        """
        if not search_query:
            return []

        # Prefer DB-backed search if function provided
        if db_search_fn is not None:
            try:
                return db_search_fn(search_query, limit=5)
            except Exception:
                # If DB search fails for any reason, fall back to in-memory
                pass

        if not all_tasks_data:
            return []

        query = search_query.lower()
        filtered = [
            task for task in all_tasks_data
            if query in task.get("title", "").lower() or
               query in task.get("description", "").lower()
        ]
        return filtered[:5]  # Limit to 5 results
    
    def update_dropdown(e):
        """Update dropdown when user types."""
        search_query = e.control.value
        
        if not search_query or len(search_query) < 2:
            # Hide dropdown
            dropdown_container_ref.current.visible = False
            dropdown_ref.current.controls.clear()
            page.update()
            return
        
        # Filter tasks
        filtered_tasks = filter_tasks(search_query)
        
        # Clear dropdown
        dropdown_ref.current.controls.clear()
        
        if filtered_tasks:
            # Add filtered tasks to dropdown
            for task in filtered_tasks:
                dropdown_ref.current.controls.append(
                    create_task_dropdown_item(task, on_task_click, search_field_ref, dropdown_container_ref, page)
                )
            dropdown_container_ref.current.visible = True
        else:
            # Show "No results"
            dropdown_ref.current.controls.append(
                ft.Container(
                    content=ft.Text("No tasks found", size=12, color="#6b7280"),
                    padding=10
                )
            )
            dropdown_container_ref.current.visible = True
        
        page.update()
    
    def on_focus(e):
        """Show dropdown when search field is focused."""
        if search_field_ref.current.value and len(search_field_ref.current.value) >= 2:
            dropdown_container_ref.current.visible = True
            page.update()
    
    # Search container with dropdown
    search_container = ft.Column([
        # Main search bar
        ft.Container(
            content=ft.Row([
                ft.Icon("search", color="#9ca3af", size=20),
                ft.TextField(
                    ref=search_field_ref,
                    hint_text="Search for Task..",
                    border=ft.InputBorder.NONE,
                    text_size=14,
                    expand=True,
                    on_change=update_dropdown,
                    on_focus=on_focus
                ),
                ft.IconButton(
                    icon="add",
                    icon_color="#6366f1",
                    bgcolor="#e0e7ff",
                    icon_size=20,
                    on_click=show_add_dialog_handler
                )
            ], spacing=10),
            bgcolor="#ffffff",
            padding=ft.padding.only(left=15, right=5, top=5, bottom=5),
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=2,
                color="#00000008",
                offset=ft.Offset(0, 1)
            )
        ),
        
        # Dropdown
        ft.Container(
            ref=dropdown_container_ref,
            content=ft.Column(
                ref=dropdown_ref,
                spacing=0,
                scroll=ft.ScrollMode.AUTO
            ),
            bgcolor="#ffffff",
            border_radius=10,
            border=ft.border.all(1, "#e5e7eb"),
            padding=5,
            visible=False,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color="#0000001a",
                offset=ft.Offset(0, 4)
            ),
            margin=ft.margin.only(top=-5)  # Pull up slightly to connect to search bar
        )
    ], spacing=0)
    
    return search_container


def create_task_dropdown_item(task, on_task_click, search_field_ref, dropdown_container_ref, page):
    """
    Create a dropdown item for a task.
    
    Args:
        task: Task dictionary
        on_task_click: Callback when task is clicked
        search_field_ref: Reference to search field
        dropdown_container_ref: Reference to dropdown container
        page: Flet page object
    
    Returns:
        ft.Container: Dropdown item
    """
    
    def handle_click(e):
        # Hide dropdown first
        dropdown_container_ref.current.visible = False
        
        # Clear search field
        search_field_ref.current.value = ""
        
        # Update page
        page.update()
        
        # Open edit dialog with the task
        on_task_click(task)
    
    # Get status color
    status_colors = {
        "completed": "#10b981",
        "pending": "#f59e0b",
        "overdue": "#ef4444"
    }
    status_color = status_colors.get(task.get("status", "pending"), "#6b7280")
    
    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon("circle", size=8, color=status_color),
                padding=ft.padding.only(left=5)
            ),
            ft.Column([
                ft.Text(
                    task.get("title", "Untitled"),
                    size=13,
                    color="#1f2937",
                    weight=ft.FontWeight.W_500,
                    no_wrap=True,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                ft.Text(
                    task.get("description", "")[:50] + ("..." if len(task.get("description", "")) > 50 else ""),
                    size=11,
                    color="#6b7280",
                    no_wrap=True,
                    overflow=ft.TextOverflow.ELLIPSIS
                ) if task.get("description") else ft.Container()
            ], spacing=2, expand=True)
        ], spacing=10),
        padding=10,
        border_radius=8,
        ink=True,
        on_click=handle_click,
        on_hover=lambda e: setattr(e.control, 'bgcolor', '#f3f4f6' if e.data == "true" else None) or page.update()
    )