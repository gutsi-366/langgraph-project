import pandas as pd
from langgraph_agent import run_agent

def main():
    print("Starting LangGraph Agent...")
    run_agent()  # This will read your CSV and generate a report

if __name__ == "__main__":
    main()

