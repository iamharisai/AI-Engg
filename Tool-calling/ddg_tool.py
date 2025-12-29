from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

response = search_tool.invoke("what is the latest score of IND-SA T20 match")

print(response)