# Importing the dependencies
from API.dependencies import *
from src.dependencies import *
from src.instances import *
from src.workers.documents.utils import *
from src.workers.documents.instances import *
from API.schemas.documents import StoreDoc, DeleteDoc
from API.utils import process_incoming_SQS_knowledge_base

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


def sqs_polling():
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


# Startup event to launch polling as a thread
@app.on_event("startup")
async def startup_event():
    logging.info("Starting SQS polling...")
    polling_thread = threading.Thread(target=sqs_polling, daemon=True)
    polling_thread.start()
    
@app.get("/")
def home():
    return "Hello from 100xSage Services!"