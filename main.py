import pandas as pd
from vanna_setup import get_agent,validate_and_run_sql
from vanna.servers.fastapi import VannaFastAPIServer

# Initialize Agent
agent = get_agent()

def scustom_run_sql(sql:str,**kwargs):
    result = validate_and_run_sql(agent,sql)
    
    if isinstance(result,str):
        return pd.DataFrame({"Message":[result]})
    
    # if isinstance(result,dict):
    #     df = result["data"]
    #     summary = result["summary"]
        
    #     # Add summary as a extra row
    #     summary_df = pd.DataFrame({col: "" for col in df.columns}, index=[0])
    #     summary_df[df.columns[0]] = f"Summary: {summary}"
    #     return pd.concat([df,summary_df],ignore_index=True)
    return result
# Assign custom runner
agent.run_sql = scustom_run_sql

# Initialize Vanna FastAPI Server
vanna_server = VannaFastAPIServer(agent)

# Run the FastAPI app
if __name__ == '__main__':
    print("Clinic Analytics API is running with SQL Validation & Error Handling...")
    vanna_server.run()