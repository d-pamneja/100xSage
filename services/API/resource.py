# Importing the dependencies
from API.dependencies import Lock,FastAPI,CORSMiddleware,ThreadPoolExecutor
from API.dependencies import HTTPException
from API.schemas.resolver import ResolverInput
from API.pollers import KB_sqs_polling,QA_sqs_polling

from src.dependencies import logging,json
from src.exception import CustomException
from src.agents.Resolver.schemas.editor import EditorOutput
from src.agents.Resolver.crew import ResolverCrew


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

@app.post("/resolve",response_model = EditorOutput)
async def resolver(userInput : ResolverInput):
    """Endpoint to recommend answer to user query if solved previosuly from threads"""
    try:
        logging.info(f"New search for input : {userInput.query}")
        result = ResolverCrew().crew().kickoff(inputs={"query": userInput.query})
        answer = json.loads(result.raw)
        logging.info(f"Recommendation generated : {answer['solution']}")
        
        return answer
    except CustomException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")