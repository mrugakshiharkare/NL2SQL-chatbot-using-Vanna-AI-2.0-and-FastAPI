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
app = getattr(vanna_server, 'app', None)    

@app.get("/health")
def health_check():
    return {"status": "Ok",
            "Database":"connected",
            "agent_memory_entries": len(agent.agent_memory.tool_uses) if agent.agent_memory else 0,
            "framework":"Vanna 2.0 with FastAPI"
            }
    
#5. Run the server
if __name__ == '__main__':
    print("Clinic Analytics API is running on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)