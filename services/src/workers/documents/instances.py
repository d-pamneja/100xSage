from src.dependencies import time,boto3,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,PINECONE_KNOWLEDGE_BASE_INDEX_NAME,KNOWLEDGE_BASE_MODIFICATION_QUEUE_URL,KNOWLEDGE_BASE_MODIFICATION_NOTIFICATIONS_ARN
from src.instances import pc

while not pc.describe_index(PINECONE_KNOWLEDGE_BASE_INDEX_NAME).status['ready']:
    time.sleep(1)
    
# Pinecone Index instance
index_knowledge_base = pc.Index(PINECONE_KNOWLEDGE_BASE_INDEX_NAME)

# AWS SQS and SNS instances
knowledge_base_SQS_client = boto3.resource(
    'sqs',
    region_name = "ap-south-1",
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

knowledge_base_SQS_queue = knowledge_base_SQS_client.Queue(KNOWLEDGE_BASE_MODIFICATION_QUEUE_URL)

knowledge_base_SNS_client = boto3.resource(
    "sns",
    region_name = "ap-south-1",
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

knowledge_base_SNS_topic = knowledge_base_SNS_client.Topic(KNOWLEDGE_BASE_MODIFICATION_NOTIFICATIONS_ARN)