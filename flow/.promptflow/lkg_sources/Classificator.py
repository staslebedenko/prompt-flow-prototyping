from promptflow import tool  
import openai  
import os  
import json  
import numpy as np
from typing import Dict, Any   
  
@tool  
def my_python_tool(input1: str) -> str:   
    openai.api_key = "t1qO8ePekEylAvG"  
    openai.api_type = "azure"  
    openai.api_base = "https://stas-.openai.azure.com/"  
    openai.api_version = "2023-07-01-preview"  
    openai.api_key = "eb7bd9b4aw6"  
    num_clusters = 5  
    model = 'gpt-3.5-turbo'  
    
    input_strings = input1.split('\n') 
     
    results = 'custom python result'
  
    return results  
