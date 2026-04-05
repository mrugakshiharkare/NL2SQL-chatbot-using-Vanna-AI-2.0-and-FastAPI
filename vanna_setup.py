import os
import pandas as pd
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
        return User(id="123", email="admin@example.com", group_memberships=["admin"])

def get_agent():
    #1. LLM Service 
    llm = GeminiLlmService(
        model = "gemini-2.5-flash",
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
    registry.register_local_tool(SaveQuestionToolArgsTool(),access_groups=['admin'])
    registry.register_local_tool(SearchSavedCorrectToolUsesTool(),access_groups=['admin','user'])
    
    #5. Agent Intialization
    agent = Agent(
        config=AgentConfig(system_prompt="You are a SQL assistant for a Clinic. Use RunSqlTool to answer data questions.",allow_llm_to_see_data=True),
        llm_service = llm,
        tool_registry = registry,
        agent_memory = agent_memory,
        user_resolver = SimpleUserResolver()
    )
    return agent

# if __name__ == '__main__':
#     #Test the agent
#     try:
#         my_agent = get_agent()
#         print("Vanna 2.0 Agent succesfully initialized!")
#     except Exception as e:
#         print(f"Error initializing Vanna 2.0 Agent: {e}")

def validate_and_run_sql(agent,question_or_sql):
    #1. Generate SQL using agent
    sql_query = question_or_sql.strip()
    if not("SELECT" in sql_query.upper()):
        try:
            sql_query = agent.generate_sql(question_or_sql)
        except Exception as e:
            return f"Error generating SQL: {str(e)}"
    
    # SQL VALIDATION
    forbidden_keywords = ["INSERT","UPDATE","DELETE","DROP","ALTER","EXEC","XP_","SP_","GRANT","REVOKE","SHUTDOWN","SQLITE_MASTER"]
    clean_sql = sql_query.strip().upper()
    
    # Validation 1: Must be SELECT
    if not clean_sql.startswith("SELECT"):
        return "Security Error: Only SELECT queries are permitted."
    
    #Validation 2,3: Check for forbidden keywords and system tables
    for word in forbidden_keywords:
        if word in clean_sql:
            return f"Security Error: The query contains forbidden keyword '{word}'."
        
    
    # ERROR HANDLING & EXECUTION
    try:
        db_runner = SqliteRunner(database_path='clinic.db')
        df = db_runner.run_sql(sql_query)
        
        # Check for empty result
        if df is None or df.empty:
            return "No data found for this request."
        
        # GENERATE SUMMARY
        summary = f"Query executed successfully with {len(df)} rows returned."
        # Create summary row
        summary_row = pd.DataFrame([{col: "" for col in df.columns}])
        summary_row.iloc[0,0] = summary
        return pd.concat([df,summary_row],ignore_index=True)
       
    except Exception as e:
        return f"Database Error: {str(e)}"
