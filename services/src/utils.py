from src.instances import embedding_model
from src.exception import CustomException
from src.dependencies import sys

def get_embedding(text) :
    """
        Function to convert the text string into embeddings using text-embedding-3-small from OpenAI
    
        Args:
            text : A string which will contain either the text chunk or the user query
            
        Returns:
            vector : A vector of 1536 dimensions
    """
    
    try:
        response = embedding_model.create(
            input=text,
            model="text-embedding-3-small"
        )
        
        return response.data[0].embedding   
    
    except Exception as e:
        raise CustomException(e,sys)