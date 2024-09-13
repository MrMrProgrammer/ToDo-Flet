import flet as ft
import requests

API_URL = "http://127.0.0.1:8000/todos"

class TodoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "TODO App"

        self.todos = ft.Column()
        self.input_task = ft.TextField(label="Task", autofocus=True)

        # دکمه برای افزودن وظیفه
        self.add_button = ft.IconButton(icon=ft.icons.ADD_TASK, on_click=self.add_todo)

        # قرار دادن input و دکمه در یک Row
        self.input_row = ft.Row(
            controls=[
                self.add_button,
                self.input_task,
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # مرکز کردن محتوای Row
            spacing=10
        )

        # افزودن Row به صفحه
        self.page.add(
            ft.Column(
                controls=[
                    self.input_row,  # استفاده از Row برای قرارگیری در کنار هم
                    self.todos,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # مرکز کردن محتوای Column
                spacing=10,  # فاصله بین کنترل‌ها
            )
        )

        # بارگیری اولیه وظایف
        self.load_todos()

    def load_todos(self):
        response = requests.get(API_URL)
        if response.status_code == 200:
            todos = response.json()
            self.todos.controls = []  # پاک کردن لیست قبلی
            for todo in todos:
                # هر وظیفه را در یک Row قرار می‌دهیم
                todo_row = ft.Row(
                    controls=[
                        ft.Text(todo['task'], text_align=ft.TextAlign.RIGHT, width=300),  # راست‌چین و تنظیم عرض ثابت
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, id=todo['id']: self.delete_todo(id))
                    ],
                    alignment=ft.MainAxisAlignment.CENTER  # مرکز کردن محتوای Row
                )
                self.todos.controls.append(todo_row)
            self.page.update()

    def add_todo(self, e):
        task_text = self.input_task.value
        if task_text:
            # ارسال وظیفه جدید به API
            response = requests.post(API_URL, json={"id": len(self.todos.controls) + 1, "task": task_text})
            if response.status_code == 200:
                self.load_todos()  # بارگذاری مجدد لیست وظایف
                self.input_task.value = ""
                self.page.update()

    def delete_todo(self, todo_id):
        response = requests.delete(f"{API_URL}/{todo_id}")
        if response.status_code == 200:
            # اگر حذف موفقیت‌آمیز بود، لیست وظایف را دوباره بارگذاری کنید
            self.load_todos()

def main(page: ft.Page):
    todo_app = TodoApp(page)  # پارامتر page را به TodoApp منتقل کنید

# ft.app(target=main)

if __name__ == "__main__":
    ft.app(target=main, host="0.0.0.0", port=8001)