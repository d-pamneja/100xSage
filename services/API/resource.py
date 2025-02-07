# Importing the dependencies
from API.dependencies import Lock,FastAPI,CORSMiddleware,ThreadPoolExecutor
from API.dependencies import HTTPException,asyncio
from API.schemas.agents.resolver import ResolverInput
from API.polling.pollers import KB_sqs_polling,QA_sqs_polling
from API.utils import resolve_query
from API.discord.websocket import persist_discord_connection

from src.dependencies import logging,json
from src.exception import CustomException
from src.agents.Resolver.schemas.editor import EditorOutput


# Global Lock for SQS Messages
message_processing_lock = Lock()

# Initialising the API from FastAPI and APIRouter
app = FastAPI()
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

# Startup event to launch polling as a thread
@app.on_event("startup")
async def startup_event():
    logging.info("Starting background tasks and processes...")
    asyncio.create_task(persist_discord_connection())
    
    
    executor = ThreadPoolExecutor(max_workers=8)
    
    executor.submit(KB_sqs_polling)
    executor.submit(QA_sqs_polling)
    
        
@app.get("/")
def home():
    return "Hello from 100xSage Services!"


@app.post("/services/resolve",response_model = EditorOutput)
async def resolver(userInput : ResolverInput):
    """Endpoint to recommend answer to user query if solved previously from threads"""
    try:
        return resolve_query(userInput.query)
    except CustomException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")  