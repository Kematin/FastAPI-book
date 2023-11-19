from fastapi import APIRouter, Path, HTTPException, status, \
    Request, Depends
from fastapi.templating import Jinja2Templates
from models import Todo, TodoItems

todo_router = APIRouter()
todo_list = list()
templates = Jinja2Templates(directory="../templates/")


# arg todo get by request body
@todo_router.post("/todo", status_code=201)
async def add_task(request: Request, todo: Todo = Depends(Todo.as_form)):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)
    return templates.TemplateResponse("todo.html", {
        "request": request,
        "todos": todo_list
    })


@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_tasks(request: Request) -> dict:
    return templates.TemplateResponse("todo.html", {
        "request": request,
        "todo_list": todo_list
    })


# server get todo_id by route parameter
@todo_router.get("/todo/{todo_id}")
async def retrieve_single_task(request: Request, todo_id:
                               int = Path(..., title="The ID of the task to retrieve.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse("todo.html", {
                "request": request,
                "todo": todo
            })
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {todo_id} not found."
        )


@todo_router.put("/todo/{todo_id}", status_code=201)
async def change_task(todo_data: Todo, todo_id:
                      int = Path(..., title="The ID of the task to change")) -> dict:
    for todo in todo_list:
        if todo_id == todo.id:
            todo.item = todo_data.item
            return {"message": f"Update {todo_data}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {todo_id} not found."
        )


@todo_router.delete("/todo/{todo_id}")
async def delete_task(todo_id:
                      int = Path(..., title="The ID of the task to delete")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            index = todo_list.index(todo)
            todo_list.pop(index)
            return {"message": f"Delete {todo}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {todo_id} not found."
        )
