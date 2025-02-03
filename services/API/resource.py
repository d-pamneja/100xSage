# Importing the dependencies
from API.dependencies import Lock,FastAPI,CORSMiddleware,ThreadPoolExecutor
from src.dependencies import time,logging
from src.workers.documents.instances import knowledge_base_SQS_queue
from src.workers.QA.instances import QA_base_SQS_queue
from API.utils import process_incoming_SQS_knowledge_base,process_incoming_SQS_QA_base

# Global Lock for SQS Messages
message_processing_lock = Lock()

# Initialising the API from FastAPI and APIRouter
app = FastAPI(prefix="/services")
origins = [
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# Startup event to launch polling as a thread
@app.on_event("startup")
async def startup_event():
    logging.info("Starting SQS polling...")
    executor = ThreadPoolExecutor(max_workers=8)
    
    executor.submit(KB_sqs_polling)
    executor.submit(QA_sqs_polling)
    
@app.get("/")
def home():
    return "Hello from 100xSage Services!"