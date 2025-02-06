from src.dependencies import time
from src.workers.documents.instances import knowledge_base_SQS_queue
from src.workers.QA.instances import QA_base_SQS_queue
from API.utils import process_incoming_SQS_knowledge_base,process_incoming_SQS_QA_base

def KB_sqs_polling():
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
        
def QA_sqs_polling():
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