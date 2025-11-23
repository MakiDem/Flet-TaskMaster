import flet as ft
from datetime import datetime
import threading
import time


def create_time(page):
    """
    Create a dynamic time display component that updates every second.
    
    Args:
        page: Flet page object for updates
    
    Returns:
        ft.Container: Time display component
    """
    
    # References for dynamic updates
    time_text_ref = ft.Ref[ft.Text]()
    am_container_ref = ft.Ref[ft.Container]()
    pm_container_ref = ft.Ref[ft.Container]()
    
    def update_time():
        """Update the time display."""
        while True:
            try:
                now = datetime.now()
                hour = now.hour
                current_time = now.strftime("%I:%M")  # 12-hour format (01-12)
                
                
                # Determine AM/PM
                is_pm = hour >= 12
                
                # Update time text
                time_text_ref.current.value = current_time
                
                # Update AM/PM styling
                if is_pm:
                    # PM is active
                    am_container_ref.current.bgcolor = "#ffffff"
                    am_container_ref.current.border = ft.border.all(1, "#e5e7eb")
                    pm_container_ref.current.bgcolor = "#f3f4f6"
                    pm_container_ref.current.border = None
                else:
                    # AM is active
                    am_container_ref.current.bgcolor = "#f3f4f6"
                    am_container_ref.current.border = None
                    pm_container_ref.current.bgcolor = "#ffffff"
                    pm_container_ref.current.border = ft.border.all(1, "#e5e7eb")
                
                # Update the page
                page.update()
                
                # Wait 1 second
                time.sleep(1)
            except Exception as e:
                print(f"Time update error: {e}")
                break
    
    # Get initial values
    now = datetime.now()
    current_time = now.strftime("%I:%M")
    is_pm = now.hour >= 12
    
    # Start background thread for time updates
    thread = threading.Thread(target=update_time, daemon=True)
    thread.start()
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Time", size=12, color="#6b7280", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Text(
                    current_time, 
                    size=24, 
                    weight=ft.FontWeight.BOLD, 
                    color="#1f2937",
                    ref=time_text_ref
                ),
                ft.Container(
                    content=ft.Text("AM", size=10, color="#6b7280"),
                    bgcolor="#f3f4f6" if is_pm else "#ffffff",
                    padding=5,
                    border_radius=5,
                    border=ft.border.all(1, "#e5e7eb") if is_pm else None,
                    ref=am_container_ref
                ),
                ft.Container(
                    content=ft.Text("PM", size=10, color="#6b7280"),
                    bgcolor="#ffffff" if is_pm else "#f3f4f6",
                    padding=5,
                    border_radius=5,
                    border=None if is_pm else ft.border.all(1, "#e5e7eb"),
                    ref=pm_container_ref
                )
            ], spacing=10)
        ], spacing=10)
    )