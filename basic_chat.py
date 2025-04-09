from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral:latest", temperature=0.7)

template = "You're a travel enthusiast, tell me a fun fact about {city}"
prompt = PromptTemplate(input_variables=["city"], template=template)

chain = prompt | llm

response = chain.invoke({"city" : "Japan"})
print(f"LLM said: {response}")