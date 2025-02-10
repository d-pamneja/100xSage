from src.dependencies import BaseModel, Field, List,Optional

class EditorOutput(BaseModel) : 
    status : int = Field(...,description="The status code of the answer given by the agent")
    relevance : bool = Field(...,description="Whether the team was able to find a potentially relevant solution or not")
    solution : Optional[str] = Field(...,description="The final output given by the team, given that they are able to find a relevant solution")
    name : Optional[str] = Field(...,description="The name of the document from which the text is refered, if the solution is relevant")
    reference : Optional[List[int]] = Field(...,description="The page number(s) from which this text is refered, if the solution is relevant")