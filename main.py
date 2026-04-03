import uvicorn
from fastapi import FastAPI
from vanna.servers.fastapi import VannaFastAPIServer
from vanna_setup import get_agent

#1. Create standard FastAPI app
app = FastAPI()

# 2. Initialize the agent
agent = get_agent()

# 3. Initialzie Vanna Server and link app to it
vanna_server = VannaFastAPIServer(agent, app=app)

# 4. Adding custom/health route
@app.get("/health")
async def health_check():
    return {
        "status":"Ok",
        "Database":"connected",
        "agent_memory_items": len(agent.agent_memory.storage) if agent.agent_memory else 0,
        "framework":"Vanna 2.0 with FastAPI"
    }

# 5. Adding root route to test agent response
@app.get("/")
async def root():
    return {"message":"Welcome to the Clinic Analytics Agent. Use /health or /chat"}
    
# 6. Run the server
if __name__ == '__main__':
    print("Clinic Analytics Agent is running on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)