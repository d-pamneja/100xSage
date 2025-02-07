from API.dependencies import json,BaseModel,Field,Dict,Union,List,Literal,Optional

class newThread(BaseModel):
    id : str = Field(...,description="The id of the new thread as given by the discord server")
    title : str = Field(...,description="The title of the new thread as given by the user")
    description : str = Field(...,description="The description of the new thread as given by the user")
    timestamp : str = Field(...,description="The timestamp when this thread was created")
    author : str = Field(...,description="The author of the thread")