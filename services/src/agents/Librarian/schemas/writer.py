from src.dependencies import BaseModel, Field, List,Optional

class WriterOutput(BaseModel) : 
    name : Optional[str] = Field(...,description="The name of the document from which the text is refered")
    reference : Optional[List[int]] = Field(...,description="The page number(s) from which this text is refered")
    content : str = Field(...,description="The content written by the writer to answer the query, given the research")