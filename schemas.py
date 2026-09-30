from typing import Optional
from fastapi import FastAPI , HTTPException
import os 
from dataclasses import dataclass 
from dotenv import load_dotenv
from pydantic import BaseModel , Field , ValidationInfo , field_validator
from openai import OpenAI

class TaskCreate(BaseModel):
    title:str = Field(min_length = 3, max_length = 50)
    priority:str = Field(default="medium", choices=["low", "medium", "high"])
    description: Optional[str] = "no description"

    @field_validator("title")
    @classmethod

    def validate_title_to_upper(cls,value:str)-> str:
        return value.upper()

task = TaskCreate(title="write documentation", priority="high")

task_dict = task.model_dump()
print("Dictionary:")
print(task_dict)
print(type(task_dict))

task_json = task.model_dump_json(indent=2)
print("JSON:")
print(task_json)
print(type(task_json))


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(min_length=3, max_length=50)
    priority: Optional[str] = Field(default="medium", choices=["low", "medium", "high"])
    description: Optional[str] = "no description"

    @field_validator("title")
    @classmethod

    def validate_title_to_upper(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            return value.upper()
        return value



class TaskResponse(BaseModel):
    task_id: int
    title: str
    priority: str
    description: str
    status: str


    @field_validator("title")
    @classmethod

    def validate_title_to_upper(cls, value: str) -> str:
        if value is not None:
            return value.upper()
