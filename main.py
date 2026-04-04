import pandas as pd
from vanna_setup import get_agent,validate_and_run_sql
from vanna.servers.fastapi import VannaFastAPIServer

#1. Initialize Agent
agent = get_agent()

def safe_run_sql_wrapper(sql:str,**kwargs):
    result = validate_and_run_sql(agent,sql)
    
    if isinstance(result,str):
        return pd.DataFrame({"Message":[result]})
    return result

agent.run_sql = safe_run_sql_wrapper

#2. Initialize Vanna FastAPI Server
vanna_server = VannaFastAPIServer(agent)

#3. Run the FastAPI app
if __name__ == '__main__':
    print("Clinic Analytics API is running with SQL Validation & Error Handling...")
    vanna_server.run()