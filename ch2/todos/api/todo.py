from fastapi import APIRouter, Path
from models import TodoItem

todo_router = APIRouter()
todo_list = list()


@todo_router.post("/todo")
async def add_task(todo: TodoItem):
    todo_list.append(todo)
    return {"message": f"Add {todo}"}


@todo_router.get("/todo")
async def retrieve_tasks() -> dict:
    return {"tasks": todo_list}


@todo_router.get("/todo/{todo_id}")
async def retrieve_single_task(todo_id:
                               int = Path(...,
                                          title="The ID of the task to retrieve.")
                               ) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"task": todo}
    else:
        return {"error": f"Task with id {todo_id} not found."}
