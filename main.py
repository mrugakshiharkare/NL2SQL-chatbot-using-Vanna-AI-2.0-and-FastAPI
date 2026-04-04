import uvicorn
from fastapi import FastAPI
from vanna.servers.fastapi import VannaFastAPIServer
from vanna_setup import get_agent

#1. Initialize Agent
agent = get_agent()

#2. Define the configurations 
config = {
    "fastapi":{
        "title":"Clinic Analytics API",
        "version":"1.0.0",
    }
}

#3. Initialize Vanna Server using config
vanna_server = VannaFastAPIServer(agent,config=config)

#4. Access app created by Vanna
app = getattr(vanna_server, '__app',getattr(vanna_server,'_app',getattr(vanna_server,"app",None)))   

if app:
    @app.get("/health")
    async def health_check():
        return {"status": "Ok",
                "Database":"connected",
                "agent_memory_entries": len(agent.agent_memory.tool_uses) if agent.agent_memory else 0,
                "framework":"Vanna 2.0 with FastAPI"
                }
    @app.get("/test-api")
    async def test_api():
        return {"message":"This is a test endpoint to verify the API is working!"}
else:
    print("Warning: Could not find internal FastAPI app to attach custom routes.")
    app =vanna_server
    
#5. Run the server
if __name__ == '__main__':
    print("Clinic Analytics API is running on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)