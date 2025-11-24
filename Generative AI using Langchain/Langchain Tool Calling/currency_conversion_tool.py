from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_core.tools import InjectedToolArg
from typing import Annotated
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
EXCHANGERATE_API_KEY= os.getenv("EXCHANGERATE_API_KEY")
# Tool Creation

# Tool 1: for getting cureency conversion factor
@tool
def get_conversion_factor(base_currency:str,target_currency:str)->float:
    """
    This function fecthes the currency conversion factor between the given 
    base currency and target currency.
    """
    url=f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base_currency}/{target_currency}"
    response= requests.get(url)
    return response.json()

# print(get_conversion_factor.invoke({'base_currency':'USD','target_currency':'PKR'}))

# Tool 2: for calculation of currency conversion
@tool
def convert_currency(base_value: float, conversion_rate:Annotated[float,InjectedToolArg])->float:
    """Given a currency conversion rate this function calculates the target currency value
    from given base currecy value"""
    return base_value*conversion_rate

# print(convert_currency.invoke({'base_value':30,'conversion_rate':282.33}))

# Tool Binding
llm= ChatGoogleGenerativeAI(model='gemini-2.5-flash')
llm_with_tools= llm.bind_tools([get_conversion_factor,convert_currency])

# Tool Calling
query= HumanMessage('What is the conversion factor between USD and PKR and based on that can you convert 500 USD to PKR')
messages=[query]
result= llm_with_tools.invoke(messages)
messages.append(result)

# Tool Execution
for tool_call in result.tool_calls:
    if tool_call['name']== "get_conversion_factor":
        tool_message_1= get_conversion_factor.invoke(tool_call)
        messages.append(tool_message_1)
        conversion_rate= json.loads(tool_message_1.content)['conversion_rate']
    if tool_call['name']== "convert_currency":
        tool_call['args']['conversion_rate']=conversion_rate
        tool_message_2= convert_currency.invoke(tool_call)
        messages.append(tool_message_2)

# Final Call
final_result= llm_with_tools.invoke(messages)
print(final_result.text)
