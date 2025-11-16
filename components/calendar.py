import flet as ft
import calendar
from datetime import datetime

def create_calendar():
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        current_day = now.day
        
        cal = calendar.monthcalendar(current_year, current_month)
        month_name = calendar.month_name[current_month]
        
        calendar_widget = ft.Column(spacing=5)
        
        # Month header with navigation
        header = ft.Container(
            content=ft.Row([
                ft.Text(f"{month_name} {current_year}", 
                       size=14, 
                       weight=ft.FontWeight.BOLD,
                       color="#5b21b6"),
                ft.Container(expand=True),
                ft.IconButton(icon="chevron_left", icon_size=16, icon_color="#9ca3af"),
                ft.IconButton(icon="chevron_right", icon_size=16, icon_color="#9ca3af"),
            ], alignment="spaceBetween"),
            padding=ft.padding.only(bottom=10)
        )
        calendar_widget.controls.append(header)
        
        # Days of week
        days_row = ft.Row(spacing=8, alignment="center")
        for day in ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]:
            days_row.controls.append(
                ft.Container(
                    content=ft.Text(day, size=10, color="#9ca3af", weight=ft.FontWeight.W_500),
                    width=30,
                    alignment=ft.alignment.center
                )
            )
        calendar_widget.controls.append(days_row)
        
        # Calendar days
        for week in cal:
            week_row = ft.Row(spacing=8, alignment="center")
            for day in week:
                if day == 0:
                    week_row.controls.append(ft.Container(width=30, height=30))
                else:
                    is_today = (day == current_day)
                    week_row.controls.append(
                        ft.Container(
                            content=ft.Text(
                                str(day),
                                size=12,
                                color="#ffffff" if is_today else ("#dc2626" if day == 7 else "#374151"),
                                weight=ft.FontWeight.BOLD if is_today else ft.FontWeight.NORMAL
                            ),
                            width=30,
                            height=30,
                            bgcolor="#dc2626" if is_today else "transparent",
                            border_radius=15,
                            alignment=ft.alignment.center
                        )
                    )
            calendar_widget.controls.append(week_row)
        
        return calendar_widget