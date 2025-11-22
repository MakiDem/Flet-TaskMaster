# Check for overdue tasks on startup
from components.notification import NotificationManager

def check_overdue_tasks(notif_manager, all_tasks_data):
    overdue = [task for task in all_tasks_data if task["status"] == "overdue"]
    if overdue:
        notif_manager.show(
            f"You have {len(overdue)} overdue task(s)!",
            notification_type="warning",
            duration=5
        )