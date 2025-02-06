from API.dependencies import json,BaseModel,Field,Dict,Union,List,Literal,Optional

class ResolverInput(BaseModel):
    query : str = Field(...,description="The title and text given by the user")