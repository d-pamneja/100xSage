from src.logger import logging
from API.dependencies import validators,json,sys,HTTPException
from src.exception import CustomException
from API.schemas.documents import SQSMessageAttributes
from src.workers.documents.utils import load_data,chunk_data,create_vectors,upsert_vectors,delete_vectors
from src.workers.documents.instances import knowledge_base_SQS_queue, knowledge_base_SNS_topic

# Knowledge Base Processing
def process_post_message_knowledge_base(message_info: dict):
    link = message_info["link"]["StringValue"]

    if not validators.url(link):
        raise CustomException("Invalid URL provided to access file.", sys.exc_info())

    key = message_info["key"]["StringValue"]
    properties = json.loads(message_info["properties"]["StringValue"])
    userID = properties["user_id"]
    name = properties["name"]
    doc_type = properties["doc_type"]

    
    if(validators.url(link)):
        key = key.replace(" ", "_")
      
        all_documents = load_data(link,doc_type)
        logging.info("Initial document chunk set.")

        all_chunked_documents = chunk_data(all_documents)
        logging.info("Chunked documents set.")
        
        vectors = create_vectors(all_chunked_documents,key,userID,name,doc_type)
        logging.info("Records list created.")
        
        record_status = upsert_vectors(vectors)
        final_upload_status = {"response": {"upserted_count": record_status.get('upserted_count', 0)}}
        logging.info("Records uploaded.")
        
    else :
        raise HTTPException(status_code=400, detail="Invalid link type")
    
    
    if final_upload_status["response"]["upserted_count"] > 0:
        logging.info("Document Successfully Upserted at VectorDB")

        push_notification = {"status": 201, "detail": "Your document has been added to the analysis database."}
        sns_notification_response = knowledge_base_SNS_topic.publish(
            Message=json.dumps(push_notification),
            Subject="POST Document Notification",
            MessageAttributes={"key": {"DataType": "String", "StringValue": key}},
        )

        if sns_notification_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            success_message = "Document successfully added to the analysis database and notification sent to user."
            return {"statusCode": 200, "body": json.dumps({"message": success_message})}
        else:
            raise CustomException("An error occurred while sending the notification to the user")
    else:
        raise CustomException("An error occurred while upserting the vector")

def process_delete_message_knowledge_base(message_info: dict):
    key = message_info["key"]["StringValue"]

    key = key.replace(" ", "_")
    final_response = delete_vectors(key)
    if(final_response=={}):
        logging.info(f"All records associated with {key} deleted successfully")

        push_notification = {"status": 200, "detail": "Your document has been deleted from the analysis database."}
        sns_notification_response = knowledge_base_SNS_topic.publish(
            Message=json.dumps(push_notification),
            Subject="DELETE Document Notification",
            MessageAttributes={"key": {"DataType": "String", "StringValue": key}},
        )

        if sns_notification_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                success_message = "Document successfully deleted from the analysis database and notification sent to user."
                return {"statusCode": 200, "body": json.dumps({"message": success_message})}
        else:
            raise CustomException("An error occurred while sending the notification to the user")
    else:
        raise HTTPException(status_code=400, detail="Could not delete vectors from pinecone index")
    

def process_incoming_SQS_knowledge_base(message: SQSMessageAttributes):
    request_type = message.body
    message_info = message.message_attributes

    if request_type and message_info:
        if request_type not in ["POST", "DELETE"]:
            raise CustomException("Invalid request type received from SQS message.")
        else:
            if request_type == "POST":
                res = process_post_message_knowledge_base(message_info)
                if res["statusCode"] == 200:
                    body = json.loads(res["body"])
                    logging.info(body["message"])
                    deleteMessage = knowledge_base_SQS_queue.delete_messages(Entries=[{"Id": message.message_id, "ReceiptHandle": message.receipt_handle}])
                    
                    if deleteMessage["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        logging.info("Message deleted from SQS post processing")
                        
                    else:
                        raise CustomException("An error occurred while deleting the message from SQS post processing")
                else:
                    raise CustomException("An error occurred while processing the post request")
                
            elif request_type == "DELETE":
                res = process_delete_message_knowledge_base(message_info)
                if res["statusCode"] == 200:
                    body = json.loads(res["body"])
                    logging.info(body["message"])
                    deleteMessage = knowledge_base_SQS_queue.delete_messages(Entries=[{"Id": message.message_id, "ReceiptHandle": message.receipt_handle}])
                    
                    if deleteMessage["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        logging.info("Message deleted from SQS post processing")
                        
                    else:
                        raise CustomException("An error occurred while deleting the message from SQS post processing")
                else:
                    raise CustomException("An error occurred while processing the delete request")
                
                
# QA Base Processing
def process_post_message_QA_base(message_info: dict):
    link = message_info["link"]["StringValue"]

    if not validators.url(link):
        raise CustomException("Invalid URL provided to access file.", sys.exc_info())

    key = message_info["key"]["StringValue"]
    properties = json.loads(message_info["properties"]["StringValue"])
    userID = properties["user_id"]
    name = properties["name"]
    doc_type = properties["doc_type"]

    
    if(validators.url(link)):
        key = key.replace(" ", "_")
      
        all_documents = load_data(link,doc_type)
        logging.info("Initial document chunk set.")

        all_chunked_documents = chunk_data(all_documents)
        logging.info("Chunked documents set.")
        
        vectors = create_vectors(all_chunked_documents,key,userID,name,doc_type)
        logging.info("Records list created.")
        
        record_status = upsert_vectors(vectors)
        final_upload_status = {"response": {"upserted_count": record_status.get('upserted_count', 0)}}
        logging.info("Records uploaded.")
        
    else :
        raise HTTPException(status_code=400, detail="Invalid link type")
    
    
    if final_upload_status["response"]["upserted_count"] > 0:
        logging.info("Document Successfully Upserted at VectorDB")

        push_notification = {"status": 201, "detail": "Your document has been added to the analysis database."}
        sns_notification_response = knowledge_base_SNS_topic.publish(
            Message=json.dumps(push_notification),
            Subject="POST Document Notification",
            MessageAttributes={"key": {"DataType": "String", "StringValue": key}},
        )

        if sns_notification_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            success_message = "Document successfully added to the analysis database and notification sent to user."
            return {"statusCode": 200, "body": json.dumps({"message": success_message})}
        else:
            raise CustomException("An error occurred while sending the notification to the user")
    else:
        raise CustomException("An error occurred while upserting the vector")