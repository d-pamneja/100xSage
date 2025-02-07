from src.dependencies import time,CustomException
from src.workers.documents.instances import knowledge_base_SQS_queue
from src.workers.QA.instances import QA_base_SQS_queue
from API.polling.utils import process_incoming_SQS_knowledge_base,process_incoming_SQS_QA_base

def KB_sqs_polling():
    """
        Function to poll the knowledge base SQS queue for incoming. This function will be run as a thread
        as it allows us to poll the queue for incoming messages and process them accordingly.
    """
    try :
        while True:
            response = knowledge_base_SQS_queue.receive_messages(
                MaxNumberOfMessages=1,
                MessageAttributeNames=["All"],
                VisibilityTimeout=10,
            )

            if response:
                message = response[0]
                if(message is not None):
                    process_incoming_SQS_knowledge_base(message)

            time.sleep(5) 
    except CustomException as e:
        raise CustomException("An error occurred while commencing polling for knowledge base SQS messages")
        
def QA_sqs_polling():
    """
        Function to poll the QA base SQS queue for incoming. This function will be run as a thread
        as it allows us to poll the queue for incoming messages and process them accordingly.
    """
    try:
        while True:
            response = QA_base_SQS_queue.receive_messages(
                MaxNumberOfMessages=1,
                MessageAttributeNames=["All"],
                VisibilityTimeout=10,
            )

            if response:
                message = response[0]
                if(message is not None):
                    process_incoming_SQS_QA_base(message)

            time.sleep(5) 
    except CustomException as e:
        raise CustomException("An error occurred while commencing polling for QA base SQS messages")