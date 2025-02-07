from API.dependencies import json,BaseModel,Field,Dict,Union,List,Literal,Optional

# Data Models for Input and Output
class StoreDocumentQuery(BaseModel):
    file_url: str = Field(..., description="The AWS link of the document")
    file_type: str = Field(..., description="The file type of the document (e.g., 'text' or 'pdf')")

class DocumentObject(BaseModel):
    page_content: str = Field(..., description="The content of a single document page or chunk")
    metadata: Dict[str, Union[str, float, int]] = Field(..., description="Metadata such as source and page information")

class DocumentList(BaseModel):
    documents: List[DocumentObject] = Field(..., description="A collection of document objects representing the loaded and chunked content")
    
class GetEmbeddings(BaseModel):
    text : str = Field(...,description="The text string which has to be converted to an embedding")
    
class DocInfo(BaseModel):
    key : str = Field(...,description="The exact location of the file in AWS cloud")
    userID : str = Field(...,description="The userID of the user")
    name : str = Field(...,description="The name of the document")
    type: str = Field(..., description="The file type of the document (e.g., 'text' or 'pdf')")
    
class Embedding(BaseModel):
    vector : List[float] = Field(...,description="The embedding vector of any gives text chunk")
    
class PineconeRecord(BaseModel):
    id: str = Field(..., description="The unique identifier for the record")
    values: Embedding = Field(..., description="The embedding vector for the text chunk")
    metadata: Dict[str, Union[str, float, int]] = Field(
        ...,
        description="Metadata associated with the record, such as user ID, document type, key, chunk content, page number, and chunk number"
    )

class PineconeRecordsList(BaseModel):
    records: List[PineconeRecord] = Field(..., description="A list of Pinecone records to be upserted")
   
# Store Document Input Class
class StoreDoc(BaseModel):
    initial_query : StoreDocumentQuery = Field(...,description="The initial data which contains the the link of document and it's type")
    doc_info : DocInfo = Field(...,description="The important metadata of the document which will be used in records.")

# Delete Document Input Class
class DeleteDoc(BaseModel):
    key : str = Field(...,description="The prefix of all ids of the given document")
    
# Delete Document Output
class DeleteResponse(BaseModel):
    response : str = Field(...,description="The final confirmation of the deletion of given records in vectorDB")

# Store Document Output
class UpsertResponse(BaseModel):
    response : Dict[str,int] = Field(...,description="The final confirmation of the number of records upserted in vectorDB")
    
# # SQS Message
class MessageAttributeValue(BaseModel):
    StringValue: str
    DataType: Literal["String"]

class Properties(BaseModel):
    user_id: str
    name: str
    doc_type: str

class SQSMessageAttributes(BaseModel):
    key: Optional[MessageAttributeValue]
    link: Optional[MessageAttributeValue]
    properties: Optional[MessageAttributeValue]
    
    def get_parsed_properties(self) -> Optional[Properties]:
        """Helper method to parse the properties JSON string if it exists"""
        if self.properties:
            return Properties.model_validate(json.loads(self.properties.StringValue))
        return None
