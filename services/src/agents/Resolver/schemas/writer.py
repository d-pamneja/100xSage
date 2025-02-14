from src.dependencies import BaseModel, Field,Optional

class WriterOutput(BaseModel) : 
    id : Optional[str] = Field(...,description="The discord ID of the thread, from which this document is quoted")
    content : str = Field(...,description="The content written by the writer to answer the query, given the research")