from src.dependencies import BaseModel, Field, List

class QueryInput(BaseModel) :
    query : str = Field(...,description = "The query which has to be passed to the tool")

class ResearcherDocuments(BaseModel) : 
    id : str = Field(...,description="The discord ID of the thread, from which this document is quoted")
    score : float = Field(...,description="The score implying the relvance of this document to the given query, with 0 being the lowest and 1 being the highest, and -1 being irrelevant")
    question : str = Field(...,description="The question which was asked in that document")
    answer : str = Field(...,description="The answer which was provided earlier in that document")
    
    
class ResearcherOutput(BaseModel) : 
    research : List[ResearcherDocuments] = Field(...,description="The discord ID of the thread, from which this document is quoted")