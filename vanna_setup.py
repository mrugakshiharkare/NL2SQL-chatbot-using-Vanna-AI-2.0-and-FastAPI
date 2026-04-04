import os
from dotenv import load_dotenv
from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.google import GeminiLlmService

# To load the environment variables from the .env file
load_dotenv()

class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        # For demonstration, we return a static user. In production, this should be dynamic.
        return User(id="123", name="Test User", access_groups=["admin"])

def get_agent():
    #1. LLM Service 
    llm = GeminiLlmService(
        model = 'gemini-2.0-pro',
        api_key = os.getenv('GOOGLE_API_KEY'))
    
    # Database connection
    db_runner = SqliteRunner(database_path='clinic.db')
    db_tool = RunSqlTool(db_runner)
    
    #3.Agent Memory
    agent_memory = DemoAgentMemory()
    
    #4. Tool Registry
    registry = ToolRegistry()
    registry.register_local_tool(db_tool,access_groups=['admin','user'])
    registry.register_local_tool(VisualizeDataTool(),access_groups=['admin','user'])
    registry.register_local_tool(SaveQuestionToolArgsTool(),access_groups=['admin','user'])
    registry.register_local_tool(SearchSavedCorrectToolUsesTool(),access_groups=['admin','user'])
    
    #5. Agent Intialize
    agent = Agent(
        config=AgentConfig(),
        llm_service = llm,
        tool_registry = registry,
        agent_memory = agent_memory,
        user_resolver = SimpleUserResolver()
    )
    return agent

if __name__ == '__main__':
    #Test the agent
    try:
        my_agent = get_agent()
        print("Vanna 2.0 Agent succesfully initialized!")
    except Exception as e:
        print(f"Error initializing Vanna 2.0 Agent: {e}")
