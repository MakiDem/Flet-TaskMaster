

def get_priority_color(priority):
        colors = {
            "high": "#ef4444",
            "medium": "#f59e0b",
            "low": "#22c55e"
        }
        return colors.get(priority, "#6b7280")
    
def get_status_color(status):
    colors = {
        "completed": "#22c55e",
        "pending": "#f59e0b",
        "overdue": "#ef4444"
    }
    return colors.get(status, "#6b7280")