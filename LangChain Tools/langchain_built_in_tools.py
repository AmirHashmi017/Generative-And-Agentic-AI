# DuckDuckGo Search Run for web search
from langchain_community.tools import DuckDuckGoSearchRun

search_tool= DuckDuckGoSearchRun()

result= search_tool.invoke("Top new in Pakistan today")

print(result)

# Shell tool for running shell commands
from langchain_community.tools import ShellTool

shell_tool= ShellTool()

result= shell_tool.invoke('whoami')

print(result)