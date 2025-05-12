from pydantic import BaseModel,Field
from enum import Enum
from datetime import datetime


class ModelName(str,Enum):
    Mistral_AI = "mistralai/Mistral-7B-Instruct-v0.1"
    LLAMA_70B= "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.LLAMA_70B)

class QueryResponse(BaseModel):
    answer:str
    session_id:str
    model:ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int


# Pydantic is a powerful library for data validation and settings management,
# especially useful when working with structured data (like JSON) or data models in Python.
# BaseModel and Field are two fundamental components of Pydantic.

# ✅ Field:
# Field is used to add additional metadata or constraints to the fields of a model.

# You can use Field to define default values, validate constraints (e.g., min_length, max_length, gt, lt), and even provide descriptions for your fields.

# Example:

# from pydantic import BaseModel, Field

# class Product(BaseModel):
#     name: str = Field(..., max_length=100)  # Field with max length
#     price: float = Field(..., gt=0)  # Price must be greater than 0
#     description: str = Field(default="No description provided", max_length=500)


# product = Product(name="Laptop", price=999.99)
# print(product.dict())

# In this example:

# If you tried to create a Product with an invalid type (e.g., passing a string for price), Pydantic would automatically raise a validation error.

# name has a maximum length of 100 characters.

# price must be greater than 0 (gt=0).

# description has a default value and a maximum length of 500 characters.

