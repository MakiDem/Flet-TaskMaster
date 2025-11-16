import flet as ft

def main(window: ft.Page):
    window.title = "Task Manager"
    window.vertical_alignment = ft.MainAxisAlignment.START
    window.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    window.padding = 20
    window.scroll = ft.ScrollMode.AUTO

    window.window.width = 1400
    window.window.height = 900
    window.window.center()
    
    header = ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD)
    window.add(header)

ft.app(target=main)