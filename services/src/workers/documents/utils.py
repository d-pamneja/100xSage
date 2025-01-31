from src.workers.documents.instances import index_knowledge_base
from src.instances import embedding_model
from src.dependencies import os,sys,requests,TextLoader,PyPDFLoader,RecursiveCharacterTextSplitter
from src.exception import CustomException
from src.logger import logging

def load_data(file_url, file_type):
    """
    Function to classify the file as either a text or PDF file, download it from a given URL,
    and return the finalised collection of documents.

    Args:
        file_url (str): The URL of the file to be classified, either a .pdf or .txt file
        file_type (str): The type of file ('text' or 'pdf')

    Returns:
        list: A list of documents, where each document contains:
            1. page_content: The text document in the given page
            2. metadata: The information about the file
                a. source: The location of the file
                b. page: The page number of the file (will always be 0 for a .txt file)
    """

    try:
        response = requests.get(file_url)
        response.raise_for_status()  

        temp_filename = f"temp_check"
        
        extension = ".txt" if file_type == "text" else ".pdf"
        temp_filepath = f"./temp/{temp_filename}{extension}"   

        with open(temp_filepath, "wb") as temp_file:
            temp_file.write(response.content)

        if file_type == "text":
            data_loader = TextLoader(temp_filepath)
            data = data_loader.load()
            data[0].metadata["page"] = 0
            return data

        elif file_type == "pdf":
            data_loader = PyPDFLoader(temp_filepath)
            data = data_loader.load()
            return data
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
            
            
def chunk_data(data):
    """
        Function to break a document collection into chunks of documents, which will make each 
        chunk into a fixed character length with certain overlap
    
        Args:
            data : A list of document type objects as defined in load_data
            
        Returns:
            list: A list of chunks with each chunk as a documents with unique chunk ID
    """
    
    try:
        text_split = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
        text_chunks = text_split.split_documents(data)

        return text_chunks      
    
    except Exception as e:
        raise CustomException(e,sys)
    

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
    
def create_vectors(text_chunks,KEY,USER_ID,COURSE_ID,TOPIC_NAME,DOCUMENT_NAME,DOCUMENT_TYPE):
    """
        Function to convert the text chunks into pinecone records to upsert into our index
    
        Args:
            text_chunks : A string which will contain either the text chunk or the user query
            KEY : The exact location of the file in AWS cloud, used to store in metadata of record
            USER_ID : The userID of the user who created this document, used to store in metadata of record
            COURSE_ID : The courseID of the course the chunk is from, used to store in metadata of record
            TOPIC_NAME : The topic name of the topic the chunk is from, used to store in metadata of record
            DOCUMENT_NAME : The name of the document the chunk is from, used to store in metadata of record
            DOCUMENT_TYPE : The type of document the chunk is from, used to store in metadata of record
            
        Returns:
            vectors : A final collection of pinecone records
    """
    
    try:
        vectors = []
        chunk_num = 0
        
        for chunk in text_chunks: 
            page_num = chunk.metadata["page"]
            
            entry = {}
            entry["id"] = f"{KEY}_PAGE_{page_num}_CHUNK_{chunk_num}"
            entry["values"] = get_embedding(chunk.page_content)
            entry["metadata"] = {
                "userID" : USER_ID,
                "courseID" : COURSE_ID,
                "topic_name" : TOPIC_NAME,
                "type" : DOCUMENT_TYPE,
                "document_name" : DOCUMENT_NAME,
                "key" : KEY,
                "chunk" : chunk.page_content,
                "page_number" : chunk.metadata["page"],
                "chunk_number" : chunk_num
            }
            
            chunk_num += 1
            vectors.append(entry)
            
        return vectors

    except Exception as e:
        raise CustomException(e,sys)
    
def upsert_vectors(vectors):
    """
        Function to upsert the vector records into the index
    
        Args:
            vectors : The collection of records as defined above
            
    """
    
    try:

        record_status = index_knowledge_base.upsert(
            vectors=vectors
        )  
        
        upserted_count = record_status.get("upserted_count", len(vectors))
        logging.info(f"Total records upserted successfully: {upserted_count}")
        
        return record_status
    
    except Exception as e:
        raise CustomException(e,sys)
    
def delete_vectors(key):
    """
        Function to delete vectors associated to a given document
    
        Args:
            key : The exact location of the file in AWS cloud, used to match prefix of records
            
    """
    
    try:
        res = index_knowledge_base.delete([ids for ids in index_knowledge_base.list(prefix=key)])
        return res
    
    except Exception as e:
        raise CustomException(e,sys)