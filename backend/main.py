from fastapi import FastAPI, Request
from langsmith_integration import trace_with_langsmith
from langsmith import Client
from langsmith.agents.multiprodigy_agent import create_multiprodigy_agent
from langsmith.chains.multiprodigy_chain import tools

app = FastAPI()
client = Client()

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    query = data.get("query", "")
    
    agent = create_multiprodigy_agent(tools)
    result = agent.run(query)
    return {"response": result}
