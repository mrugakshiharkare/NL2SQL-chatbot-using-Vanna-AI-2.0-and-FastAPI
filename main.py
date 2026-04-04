import pandas as pd
from vanna_setup import get_agent,validate_and_run_sql
from vanna.servers.fastapi import VannaFastAPIServer

# Initialize Agent
agent = get_agent()

def safe_run_sql_wrapper(sql:str,**kwargs):
    result = validate_and_run_sql(agent,sql)
    
    if isinstance(result,str):
        return pd.DataFrame({"Message":[result]})
    
    if isinstance(result,dict):
        df = result["data"]
        summary = result["summary"]
        
        # Add summary as a extra row
        summary_df = pd.DataFrame("Summary":[summary])
        return pd.concat([df,summary_df],ignore_index=True)
    return result

# Wrapper 
agent.run_sql = safe_run_sql_wrapper

# Initialize Vanna FastAPI Server
vanna_server = VannaFastAPIServer(agent)

# Run the FastAPI app
if __name__ == '__main__':
    print("Clinic Analytics API is running with SQL Validation & Error Handling...")
    vanna_server.run()