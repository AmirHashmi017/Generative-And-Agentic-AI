from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic import hub
import requests
from dotenv import load_dotenv
import os

load_dotenv()
WEATHERSTACK_API_KEY= os.getenv("WEATHERSTACK_API_KEY")

search_tool= DuckDuckGoSearchRun()

@tool
def get_weather_data(city:str)->str:
    """
    This function fetches the weather data for a given city
    """
    url= f"https://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={city}"
    response= requests.get(url)
    return response.json()

llm= ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt= hub.pull("hwchase17/react") # react is a design pattern of agent means Reason and Act

# Agent plans decides things
agent= create_react_agent(
    llm= llm,
    tools= [search_tool,get_weather_data],
    prompt= prompt
)

# Agent executor takes actions
agent_executor= AgentExecutor(
    agent= agent,
    tools= [search_tool,get_weather_data],
    verbose= True
)

response= agent_executor.invoke({"input": "Find the current weather condition of capital of Pakistan"})
print(response)