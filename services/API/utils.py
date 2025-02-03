from src.logger import logging
from API.dependencies import validators,json,sys,HTTPException
from src.exception import CustomException
from API.schemas.documents import SQSMessageAttributes
from src.workers.documents.utils import load_data,chunk_data,create_KB_vectors,upsert_KB_vectors,delete_KB_vectors
from src.workers.documents.instances import knowledge_base_SQS_queue, knowledge_base_SNS_topic
from src.workers.QA.instances import QA_base_SQS_queue,QA_base_SNS_topic,QA_base_S3_client
from src.workers.QA.utils import load_QA_data,get_QA,create_QA_vector,upsert_QA_vectors,delete_QA_vectors
from src.dependencies import QA_BASE_BUCKET_NAME

# Knowledge Base Processing
def process_post_message_knowledge_base(message_info: dict):
    link = message_info["link"]["StringValue"]

    if not validators.url(link):
        raise CustomException("Invalid URL provided to access file.", sys.exc_info())

    key = message_info["key"]["StringValue"]
    properties = json.loads(message_info["properties"]["StringValue"])
    userID = properties["user_id"]
    courseID = properties["course_id"]
    topic_name = properties["topic_name"]
    filename = properties["name"]
    doc_type = properties["doc_type"]

    
    if(validators.url(link)):
        key = key.replace(" ", "_")
      
        all_documents = load_data(link,doc_type)
        logging.info("Initial document chunk set.")

        all_chunked_documents = chunk_data(all_documents)
        logging.info("Chunked documents set.")
        
        vectors = create_KB_vectors(all_chunked_documents,key,userID,courseID,topic_name,filename,doc_type)
        logging.info("Records list created.")
        
        record_status = upsert_KB_vectors(vectors)
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
    final_response = delete_KB_vectors(key)
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
        raise Exception("Invalid URL provided to access file.")

    key = message_info["key"]["StringValue"]
    properties = json.loads(message_info["properties"]["StringValue"])
    adminID = properties["admin_id"]
    courseID = properties["course_id"]
    topicID = properties["topic_id"]
    QA_ID = properties["thread_id"]

    
    if(validators.url(link)):
        key = key.replace(" ", "_")
      
        conversation = load_QA_data(link)
        logging.info("Initial conversation loaded")

        QA = get_QA(conversation,QA_ID)
        logging.info("Chunked documents set.")
        
        vector = create_QA_vector(QA,adminID,courseID,topicID)
        logging.info("Records list created.")
        
        record_status = upsert_QA_vectors(vector)
        final_upload_status = {"response": {"upserted_count": record_status.get('upserted_count', 0)}}
        logging.info("Records uploaded.")
        
    else :
        raise Exception(status_code=400, detail="Invalid link type")
    
    
    if final_upload_status["response"]["upserted_count"] > 0:
        logging.info("Document Successfully Upserted at VectorDB")
        
        # QA S3 File Update
        summarisedThread = {}
        summarisedThread["thread_id"] = QA_ID
        QA_Pair = {
            "question" : vector["metadata"]["question"],
            "answer" : vector["metadata"]["answer"]
        }
        
        summarisedThread["content"] = QA_Pair
        
        updateResponse = QA_base_S3_client.put_object(
            Bucket = QA_BASE_BUCKET_NAME,
            Key = key,
            Body = json.dumps(summarisedThread)
        )
        
        if updateResponse["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logging.info("QA Pair successfully updated in S3")

            push_notification = {"status": 201, "detail": "Your QA has been added to the analysis database."}
            sns_notification_response = QA_base_SNS_topic.publish(
                Message=json.dumps(push_notification),
                Subject="POST QA Notification",
                MessageAttributes={"key": {"DataType": "String", "StringValue": key}},
            )

            if sns_notification_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                success_message = "QA Pair successfully added to the analysis database and notification sent to user."
                return {"statusCode": 200, "body": json.dumps({"message": success_message})}
            else:
                raise CustomException("An error occurred while sending the notification to the user")
        else :
            raise CustomException("An error occurred while updating the QA pair in S3")
    else:
        raise CustomException("An error occurred while upserting the vector")
 
def process_delete_message_QA_base(message_info: dict):
    key = message_info["key"]["StringValue"]

    properties = json.loads(message_info["properties"]["StringValue"])
    adminID = properties["admin_id"]
    courseID = properties["course_id"]
    topicID = properties["topic_id"]
    QA_ID = properties["thread_id"]
    
    final_response = delete_QA_vectors(QA_ID,adminID,courseID,topicID)
    if(final_response=={}):
        logging.info(f"All records associated with {key} deleted successfully")

        push_notification = {"status": 200, "detail": "Your QA has been deleted from the analysis database."}
        sns_notification_response = QA_base_SNS_topic.publish(
            Message=json.dumps(push_notification),
            Subject="DELETE QA Notification",
            MessageAttributes={"key": {"DataType": "String", "StringValue": key}},
        )

        if sns_notification_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                success_message = "QA successfully deleted from the analysis database and notification sent to user."
                return {"statusCode": 200, "body": json.dumps({"message": success_message})}
        else:
            raise CustomException("An error occurred while sending the notification to the user")
    else:
        raise CustomException(status_code=400, detail="Could not delete vectors from pinecone index")
    
def process_incoming_SQS_QA_base(message : SQSMessageAttributes):
    request_type = message.body
    message_info = message.message_attributes

    if request_type and message_info:
        if request_type not in ["POST", "DELETE"]:
            raise CustomException("Invalid request type received from SQS message.")
        else:
            if request_type == "POST":
                res = process_post_message_QA_base(message_info)
                if res["statusCode"] == 200:
                    body = json.loads(res["body"])
                    logging.info(body["message"])
                    deleteMessage = QA_base_SQS_queue.delete_messages(Entries=[{"Id": message.message_id, "ReceiptHandle": message.receipt_handle}])
                    
                    if deleteMessage["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        logging.info("Message deleted from SQS post processing")
                        
                    else:
                        raise CustomException("An error occurred while deleting the message from SQS post processing")
                else:
                    raise CustomException("An error occurred while processing the post request")
                
            elif request_type == "DELETE":
                res = process_delete_message_QA_base(message_info)
                if res["statusCode"] == 200:
                    body = json.loads(res["body"])
                    logging.info(body["message"])
                    deleteMessage = QA_base_SQS_queue.delete_messages(Entries=[{"Id": message.message_id, "ReceiptHandle": message.receipt_handle}])
                    
                    if deleteMessage["ResponseMetadata"]["HTTPStatusCode"] == 200:
                        logging.info("Message deleted from SQS post processing")
                        
                    else:
                        raise CustomException("An error occurred while deleting the message from SQS post processing")
                else:
                    raise CustomException("An error occurred while processing the delete request")