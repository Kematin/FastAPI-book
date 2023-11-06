from fastapi import APIRouter

todo_router = APIRouter()
todo_list = list()


@todo_router.post("/todo")
async def add_task(todo: dict) -> dict:
    todo_list.append(todo)
    return {
        "message": "Todo added successfully."
    }


@todo_router.get("/todo")
async def retrieve_tasks() -> dict:
    return {
        "tasks": todo_list
    }
