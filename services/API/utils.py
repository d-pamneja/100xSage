from src.agents.Resolver.crew import ResolverCrew
from src.agents.Resolver.schemas.editor import EditorOutput
from src.dependencies import json,logging

def resolve_query(user_query) -> EditorOutput:
    """
        Function to process user query (used internally and in API).
        
        Args:
            user_query : The user query to be resolved
            
        Returns:
            dict: The response from the resolver crew agent as defined in the schema
    """
    try:
        logging.info(f"New search for input: {user_query}")
        result = ResolverCrew().crew().kickoff(inputs={"query": user_query})
        answer = json.loads(result.raw)
        logging.info(f"Recommendation generated: {answer['solution']}")
        
        return answer
    except Exception as e:
        raise Exception(f"Internal Error: {e}")