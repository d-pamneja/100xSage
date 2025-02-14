from src.instances import openAI_client
from src.dependencies import CustomException,sys
from src.workers.resolver.config.system_instructions import system_instructions

def get_new_thread_summary(thread):
    """
        Function to generate a summary of a given thread
        
        Args:
            thread : The thread object to be summarised
            
        Returns:
            response : The summary of the thread
    """
    try:        
        text = f"""
            Title : {thread['title']}\n\n
            Description : {thread['description']}
        """
        
        response = openAI_client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {
                    "role" : "system",
                    "content" : system_instructions[0]
                },
                {
                    "role" : "user",
                    "content" : text
                    
                }
            ]
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        raise CustomException("Error occurred while generating thread summary from OpenAI Client",e)