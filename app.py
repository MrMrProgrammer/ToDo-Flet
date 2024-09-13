from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn


app = FastAPI()


class TodoItem(BaseModel):
    id: int
    task: str
    done: bool = False


todos = []


@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    return todos


@app.post("/todos", response_model=TodoItem)
def add_todo(todo: TodoItem):
    todos.append(todo)
    return todo


@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    for todo in todos:
        if todo.id == todo_id:
            todo.done = updated_todo.done
            return todo
    return None


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.id != todo_id]
    return {"message": "Deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)