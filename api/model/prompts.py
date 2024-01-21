from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict

# Create an abstract class called Audio that inherits from BaseModel
class Prompts(BaseModel):
    messages: List[Dict[str, str]]


    

