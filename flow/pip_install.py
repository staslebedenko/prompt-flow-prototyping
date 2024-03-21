import subprocess    
from promptflow import tool  
  
subprocess.check_call(["python", '-m', 'pip', 'install', '-r', 'requirements.txt'])  
  
@tool
def my_python_tool(input1: str) -> str:
  return input1
