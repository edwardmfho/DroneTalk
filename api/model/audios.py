from pydantic import BaseModel, ConfigDict
from typing import Optional

# Create an abstract class called Audio that inherits from BaseModel
class Audio(BaseModel):
    path: str
    

class Speech(Audio):
    model_config = ConfigDict(extra='allow')
    content: Optional[str] = None

class VerbalCommands(Speech):
    pass

    


    

