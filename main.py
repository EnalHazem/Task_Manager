from ast import List
from fastapi import FastAPI , HTTPException
import os
from dataclasses import asdict, dataclass 
from dotenv import load_dotenv
from pydantic import BaseModel , Field , ValidationInfo , field_validator
from openai import OpenAI
from typing import Optional
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse

load_dotenv()

dataset: dict[int, Task] = {}

app = FastAPI(title="Task Manager API", description="API for managing tasks")

def create_task(task_create: TaskCreate) -> TaskResponse:
    
    task_data = task_create.model_dump()
    task_id = len(dataset) + 1
    task = Task(task_id=task_id, **task_data)
    dataset[task_id] = task
    task_dict = asdict(task)

    return TaskResponse(**task_dict)


@app.get("/tasks",response_model=List[TaskResponse])
def get_tasks() -> List[TaskResponse]:

    return [TaskResponse(**asdict(task))
        for task in dataset.values()
    ]

@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int) -> TaskResponse:
    task = dataset.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    del dataset[task_id]
    return TaskResponse(**asdict(task), success=True, message="Task deleted successfully")

@app.patch("/tasks/{task_id}", response_model=TaskResponse)

def update_task(task_id: int, task_update: TaskUpdate) -> TaskResponse:
    task = dataset.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = dict(task_update.model_dump(exclude_unset=True))
    
    merged_task = asdict(task)
    merged_task.update(update_data)

    new_task = Task(**merged_task)
    dataset[task_id] = new_task

    return TaskResponse(**asdict(task),success = True, message = "task updated successfully")