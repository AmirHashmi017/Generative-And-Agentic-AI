

# Method 01: Creating tool using @tool Decorator
from langchain_community.tools import tool
# Step 01 - Create a function with doc string
def multiply(a,b):
    """Multiply two numbers"""
    return a*b

# Step 02 - add type hints
def multiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b

# Step 03: add tool decorator
@tool
def multiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b

result= multiply.invoke({"a":3,"b":5})
print(result)
print("Method 01: Creating tool using @tool Decorator")

print(multiply.name)
print(multiply.description)
print(multiply.args)

# What LLM seee when we attach tool
print(multiply.args_schema.model_json_schema())

# Method 02: Creating tool using Structured tool and Pydantic
from langchain_community.tools import StructuredTool
from pydantic import BaseModel,Field

class multiplyInput(BaseModel):
    a:int =Field(required=True, description="The first number to multiply")
    b:int= Field(required=True, description="The second number to add")
    

def multiply_func(a: int,b: int) ->int:
    return a*b

multiply_tool= StructuredTool.from_function(
    func=multiply_func,
    name="multiply",
    description="Multiply two numbers",
    args_schema=multiplyInput
)

result= multiply_tool.invoke({'a':3,'b':5})
print("Method 02: Creating tool using Structured tool and Pydantic")
print(result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)

# Method 03: Creating tool using Base Tool Class
from langchain_community.tools import BaseTool
from typing import Type
from pydantic import BaseModel,Field

class multiplyInput(BaseModel):
    a:int =Field(required=True, description="The first number to multiply")
    b:int= Field(required=True, description="The second number to add")

class MultiplyTool(BaseTool):
    name:str="multiply"
    description:str="Multiply two numbers"

    args_schema: Type[BaseModel]= multiplyInput

    def _run(self, a:int,b:int) ->int:
        return a*b
    
multiply_tool= MultiplyTool()
result= multiply_tool.invoke({'a':3,'b':5})
print("Method 03: Creating tool using Base Tool Class")
print(result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)