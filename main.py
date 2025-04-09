from fastapi import FastAPI
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (file:// included)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

llm = ChatOllama(model="mistral:latest", temperature=0.7)

template = '''
You're a enthusiastic and creative travel planner who is loved by everyone, customize a travel itinerary plan for {city} 
with budget {budget} for {days} days with interests like {interests}. Give the answer in this way, first some facts about the city
Day 1 - [Activity]
Day 2 - [Activity]
.
.
.
.
.
at bottom give food options best locally and some good places for favorite food {cuisine}.
'''
prompt = PromptTemplate(input_variables=["city", "budget", "days", "interests", "cuisine"], template=template)

chain = prompt | llm

class CityRequest(BaseModel):
    city: str
    budget: int
    days: int
    interests: str
    cuisine: str


@app.post("/plan")
def get_fact(request: CityRequest):
    response = chain.invoke({"city" : request.city, "budget" : request.budget, "days" : request.days, "interests" : request.interests, "cuisine" : request.cuisine})
    return {"itinerary" : response.content}