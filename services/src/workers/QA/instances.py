from src.dependencies import time,boto3,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,PINECONE_QA_BASE_INDEX_NAME,QA_BASE_MODIFICATION_QUEUE_URL,QA_BASE_MODIFICATION_NOTIFICATIONS_ARN
from src.instances import pc,openAI_client

while not pc.describe_index(PINECONE_QA_BASE_INDEX_NAME).status['ready']:
    time.sleep(1)
    
# OpenAI Instances
qa_summariser_thread = openAI_client.beta.threads.create()


# Pinecone Index instance
index_qa_base = pc.Index(PINECONE_QA_BASE_INDEX_NAME)

# AWS SQS and SNS instances
QA_base_SQS_client = boto3.resource(
    'sqs',
    region_name = "ap-south-1",
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

QA_base_SQS_queue = QA_base_SQS_client.Queue(QA_BASE_MODIFICATION_QUEUE_URL)

QA_base_SNS_client = boto3.resource(
    "sns",
    region_name = "ap-south-1",
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

QA_base_SNS_topic = QA_base_SNS_client.Topic(QA_BASE_MODIFICATION_NOTIFICATIONS_ARN)