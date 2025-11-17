import flet as ft
import threading
import time

class NotificationManager:
    def __init__(self, page):
        self.page = page
        self.notification_container = ft.Column(spacing=10)
        self.active_notifications = []
        self.page.overlay.append(self.notification_container)
    
    def show(self, message, notification_type="success", duration=3):
        """
        Show a notification
        
        Args:
            message: Text to display
            notification_type: "success", "error", "warning", "info"
            duration: Seconds to show (0 = permanent)
        """
        # Define colors and icons for each type
        styles = {
            "success": {
                "bgcolor": "#d1fae5",
                "color": "#22c55e",
                "icon": "check_circle"
            },
            "error": {
                "bgcolor": "#fee2e2",
                "color": "#ef4444",
                "icon": "error"
            },
            "warning": {
                "bgcolor": "#fef3c7",
                "color": "#f59e0b",
                "icon": "warning"
            },
            "info": {
                "bgcolor": "#dbeafe",
                "color": "#3b82f6",
                "icon": "info"
            }
        }
        
        style = styles.get(notification_type, styles["info"])
        
        # Create notification
        notification = ft.Container(
            content=ft.Row([
                ft.Icon(style["icon"], color=style["color"], size=20),
                ft.Text(message, color=style["color"], size=14, weight=ft.FontWeight.W_500, expand=True),
                ft.IconButton(
                    icon="close",
                    icon_size=16,
                    icon_color=style["color"],
                    on_click=lambda e: self.hide(notification)
                )
            ], spacing=10),
            bgcolor=style["bgcolor"],
            padding=15,
            border_radius=8,
            animate_opacity=300
        )
        
        # Add to container
        self.notification_container.controls.append(notification)
        self.active_notifications.append(notification)
        self.page.update()
        
        # Auto-hide after duration
        if duration > 0:
            def auto_hide():
                time.sleep(duration)
                self.hide(notification)
            
            threading.Thread(target=auto_hide, daemon=True).start()
    
    def hide(self, notification):
        """Hide a specific notification"""
        try:
            if notification in self.notification_container.controls:
                self.notification_container.controls.remove(notification)
            if notification in self.active_notifications:
                self.active_notifications.remove(notification)
            self.page.update()
        except Exception as e:
            print(f"Error hiding notification: {e}")
    
    def clear_all(self):
        """Clear all notifications"""
        self.notification_container.controls.clear()
        self.active_notifications.clear()
        self.page.update()
    
    def get_container(self):
        """Get the notification container to add to page"""
        return self.notification_container


def create_notification_container():
    """Create an empty notification container"""
    return ft.Column(spacing=10)