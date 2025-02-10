from src.dependencies import BaseModel, Field, List

class ResearcherDocuments(BaseModel) : 
    score : float = Field(...,description="The score implying the relvance of this document to the given query, with 0 being the lowest and 1 being the highest, and -1 being irrelevant")
    text : str = Field(...,description="The relevant text to the query in this document")
    name : str = Field(...,description="The name of the document from which the text is")
    reference : int = Field(...,description="The page number from which this text is refered")
    
class ResearcherOutput(BaseModel) : 
    research : List[ResearcherDocuments] = Field(...,description="The collection of relevant documents")