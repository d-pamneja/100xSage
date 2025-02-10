from src.dependencies import os
from src.agents.Librarian.schemas.researcher import ResearcherOutput
from src.workers.documents.instances import index_knowledge_base
from src.utils import get_embedding
from crewai.tools import tool

@tool
def fetchDocsTool(query : str) -> ResearcherOutput:
    """
        Find relevant documents for a given query and answer the query using the relevant documents.
        
        Args:
        - query (str): The search query will be in string format which will be passed straight to the LLM to find the relevant documents.
        
        Returns:
            The relevant documents from the database, given the query
    """
    query_vector = get_embedding(query)
    results = index_knowledge_base.query(
        vector=query_vector,
        top_k=5,
        include_values=False,
        include_metadata=True,
        filter={
            "userID": os.getenv("ADMIN_ID")
        }
    )
    
    relevant_texts = []
    for record in results['matches']:
        text = {
            'score': record['score'],
            'text': record['metadata']['chunk'],
            'name': record['metadata']['document_name'],
            'reference': int(record["metadata"]["page_number"]) + 1
        }
        relevant_texts.append(text)
    
    
    if not relevant_texts : 
        return [{
            'score' : -1.00,
            'text' : 'We could not find any relevant documents for the given query',
            'name' : "NA",
            'reference' : 0
        }]
        
    return relevant_texts
    