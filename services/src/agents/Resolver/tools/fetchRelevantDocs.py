from src.dependencies import BaseTool,ADMIN_ID_QA_QUERY,BaseModel,Type
from src.agents.Resolver.schemas.researcher import QueryInput,ResearcherOutput
from src.workers.QA.instances import index_qa_base
from src.utils import get_embedding
from crewai.tools import tool

@tool
def fetchDocsTool(query : str) -> ResearcherOutput:
    """
        Find relevant documents for a given query and answer the query using the relevant documents.
        
        Args:
        - query (str): The search query will be in string format which will be passed straight to the LLM to find the relevant documents.
        
        Returns:
            ResearcherOutput : The relevant documents from the database, given in the class of ResearcherOutput
    """
    query_vector = get_embedding(query)
    
    results = index_qa_base.query(
        vector = query_vector,
        top_k = 10,
        include_values = False,
        include_metadata = True,
        filter={
            "ADMIN_ID" : ADMIN_ID_QA_QUERY,
        }
    )
    
    relevant_pairs = []
    for record in results['matches']:
        pair = {}
        pair['id'] = record['metadata']['QA_ID']
        pair['score'] = record['score']
        pair['question'] = record['metadata']['question']
        pair['answer'] = record['metadata']['answer']
        relevant_pairs.append(pair)
    
    if not relevant_pairs : 
        return [{
            'id' : 'NA',
            'score' : -1.00,
            'question' : query,
            'answer' : "We could not find any relevant documents for the given query"
        }]
        
    return relevant_pairs