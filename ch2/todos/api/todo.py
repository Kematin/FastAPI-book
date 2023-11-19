from fastapi import APIRouter, Path
from models import TodoItem

todo_router = APIRouter()
todo_list = list()


# arg todo get by request body
@todo_router.post("/todo")
async def add_task(todo: TodoItem):
    todo_list.append(todo)
    return {"message": f"Add {todo}"}


@todo_router.get("/todo")
async def retrieve_tasks() -> dict:
    return {"tasks": todo_list}


# server get todo_id by route parameter
@todo_router.get("/todo/{todo_id}")
async def retrieve_single_task(todo_id:
                               int = Path(..., title="The ID of the task to retrieve.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"task": todo}
    else:
        return {"message": f"Task with id {todo_id} not found."}


@todo_router.put("/todo/{todo_id}")
async def change_task(todo_data: TodoItem, todo_id:
                      int = Path(..., title="The ID of the task to change")) -> dict:
    for todo in todo_list:
        if todo_id == todo.id:
            todo.item = todo_data.item
            return {"message": f"Update {todo_data}"}
    else:
        return {"message": f"Task with id {todo_id} not found."}


@todo_router.delete("/todo/{todo_id}")
async def delete_task(todo_id:
                      int = Path(..., title="The ID of the task to delete")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            index = todo_list.index(todo)
            todo_list.pop(index)
            return {"message": f"Delete {todo}"}
    else:
        return {"message": f"Task with id {todo_id} not found"}
