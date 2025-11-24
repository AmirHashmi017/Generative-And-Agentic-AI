from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import requests

load_dotenv()

# Tool Creation
@tool
def multiply(a:int,b:int)->int:
    """Give two numbers a and b this tool returns their product"""
    return a*b

# print(multiply.invoke({'a':2,'b':3}))

# Tool Binding

llm= ChatGoogleGenerativeAI(model='gemini-2.5-flash')
llm_with_tools= llm.bind_tools([multiply])

# Tool Calling
query= HumanMessage("Multiple 2 with 3")
messages=[query]
result= llm_with_tools.invoke(messages)
messages.append(result)
# print(result.tool_calls[0])

# Tool Execution
tool_result= multiply.invoke(result.tool_calls[0])
messages.append(tool_result)
# print(tool_result)
# print(messages)

# Final call
result= llm_with_tools.invoke(messages)
print(result.content)
