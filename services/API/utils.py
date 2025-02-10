from src.agents.Resolver.crew import ResolverCrew
from src.agents.Librarian.crew import LibrarianCrew
from src.agents.Resolver.schemas.editor import EditorOutput as ResolverOutput
from src.agents.Librarian.schemas.editor import EditorOutput as LibrarianOutput
from src.dependencies import json,logging

async def resolve_query(user_query) -> ResolverOutput:
    """
        Function to process user query (used internally and in API).
        
        Args:
            user_query : The user query to be resolved
            
        Returns:
            dict: The response from the resolver crew agent as defined in the schema
    """
    try:
        logging.info(f"New thread input: {user_query}")
        result = await ResolverCrew().crew().kickoff_async(inputs={"query": user_query})
        answer = json.loads(result.raw)
        logging.info(f"Recommendation generated: {answer['solution']}")
        
        return answer
    except Exception as e:
        raise Exception(f"Internal Error: {e}")
    
async def search_query(user_query) -> LibrarianOutput: 
    """
        Function to process user query (used internally and in API).
        
        Args:
            user_query : The user query to be resolved
            
        Returns:
            dict: The response from the librarian crew agent as defined in the schema
    """
    try:
        logging.info(f"New search for input: {user_query}")
        result = await LibrarianCrew().crew().kickoff_async(inputs={"query": user_query})
        answer = json.loads(result.raw)
        logging.info(f"Output generated: {answer['solution']}")
        
        return answer
    except Exception as e:
        raise Exception(f"Internal Error: {e}")