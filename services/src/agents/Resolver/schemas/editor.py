from src.dependencies import BaseModel, Field,Optional

class EditorOutput(BaseModel) : 
    status : int = Field(...,description="The status code of the answer given by the agent")
    relevance : bool = Field(...,description="Whether the team was able to find a potentially relevant solution or not")
    solution : Optional[str] = Field(...,description="The final output given by the team, given that they are able to find a relevant solution")
    source : Optional[str] = Field(...,description="The reference to the answer, which is the exact thread ID on discord, given that they are able to find a relevant solution ")